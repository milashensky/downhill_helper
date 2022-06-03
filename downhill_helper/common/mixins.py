import json
import uuid
import logging
import datetime
from collections import OrderedDict, Iterable

from django.db import models
from django.http import HttpResponse
from django.core.serializers import serialize
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.db.models.query import QuerySet
from django.db.models.fields.files import ImageFieldFile

from common.exceptions import PutMethodNotFound


logger = logging.getLogger(__name__)


class AuthRequierdMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class DjangoJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, HttpResponse):
            return obj.content.decode()
        if isinstance(obj, ImageFieldFile):
            return {'url': obj.url, 'name': obj.name, 'path': obj.path}
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M')
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            return str(obj.strftime('%s'))
        elif isinstance(obj, QuerySet):
            # + support of ValuesQuerySet
            return json.loads(serialize('json', obj)) if obj._fields is None else list(obj)
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, dict):
            return OrderedDict(obj)
        elif hasattr(obj, 'capitalize'):
            return obj.capitalize()
        return json.JSONEncoder.default(self, obj)


def JsonResponse(context):
    content = DjangoJSONEncoder().encode(context)
    return HttpResponse(content, content_type='application/json')


class JsonResponseMixin(object):

    def render_to_response(self, context):
        return JsonResponse(context)


class CsrfExemptMixin(object):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SerializedView(JsonResponseMixin, View):
    data = {}
    without_null = False

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        # TODO: check permision by group via self.groups
        if not self.data:
            self.data = json.loads(request.body.decode('utf-8') or '{}')
        self.filter_data = {}
        for k, v in request.GET.dict().items():
            self.filter_data[k] = v
            if ',' in str(v):
                self.filter_data[k] = v.split(',') if v else []
        response = super(SerializedView, self).dispatch(
            request, *args, **kwargs)
        fields_prop = 'fields'
        specific_fields_prop_name = f'{request.method}_fileds'.lower()
        if hasattr(self, specific_fields_prop_name):
            fields_prop = specific_fields_prop_name
        fields = getattr(self, fields_prop, None)
        if isinstance(response, (HttpResponseNotAllowed, HttpResponse)):
            return response
        elif isinstance(response, models.Model):
            response = self.serialize_item(response, fields)
        elif not isinstance(response, dict) and fields:
            response = self.serialize_items(response, fields, self.without_null)
        return self.render_to_response(response)

    @staticmethod
    def serialize_items(data, fields, without_null=False):
        if isinstance(data, Iterable):
            items, data = list(data), []
            for item in items:
                if not isinstance(item, dict):
                    item = SerializedView.serialize_item(item, fields, without_null)
                data.append(item)
        return data

    @staticmethod
    def serialize_item(item, fields, without_null=False):
        obj = {}
        for field in fields:
            if isinstance(field, dict):
                for nest, nest_fields in field.items():
                    alias, attr = SerializedView.get_item_attr(item, nest)
                    if attr is None and without_null:
                        continue
                    if isinstance(attr, Iterable):
                        obj[alias] = SerializedView.serialize_items(attr, nest_fields, without_null=False)
                    else:
                        obj[alias] = SerializedView.serialize_item(attr, nest_fields, without_null=False)
                continue
            alias, attr = SerializedView.get_item_attr(item, field)
            if attr is None and without_null:
                continue
            obj[alias] = attr
        return obj

    @staticmethod
    def get_item_attr(item, field):
        alias = field
        if ':' in field:
            parts = field.split(':')
            field = parts[0]
            alias = parts[1]
        attr = item
        for a in field.split('__'):
            attr = getattr(attr, a, None)
            if callable(attr):
                if hasattr(attr, 'all') and callable(getattr(attr, "all")):
                    attr = getattr(attr, "all")()
                else:
                    attr = attr()
        return (alias, attr)

    def vuetable_format(self, queryset, page=1, per_page=15):
        sort = self.request.GET.get('sort', '').split('|')
        if len(sort) == 2:
            queryset = queryset.order_by('%s%s' % (
                '-' if sort[1] == 'desc' else '',
                sort[0]
            ))
        items = list(queryset)
        total = len(items)
        stop = page * per_page
        start = stop - per_page
        last_page = int(total / per_page) + (total > per_page and total % per_page and 1 or 0)
        endpoint = self.request.META.get('PATH_INFO')
        return {
            'links': {
                'pagination': {
                    'total': total,
                    'per_page': per_page,
                    'current_page': page,
                    'last_page': last_page,
                    'from': start + 1,
                    'to': stop,
                    'next_page_url': None if page >= last_page else '%s?page=%d' % (endpoint, page + 1),
                    'prev_page_url': None if page <= 1 else '%s?page=%d' % (endpoint, page - 1)
                }
            },
            'data': SerializedView.serialize_items(items[start:stop], self.fields)
        }


class PutMethodMixin:
    """Mixin for PUT method with multiply actions
    """
    data = {}

    def put(self, request, *args, **kwargs):
        if not self.data:
            self.data = json.loads(request.body.decode('utf-8') or '{}')
        action = self.data.pop('action', None)
        if action:
            if hasattr(self, 'put_%s' % action):
                return getattr(self, 'put_%s' % action)(request, *args, **kwargs)
            raise PutMethodNotFound(action, self.__class__.__name__)
        return super().put(request, *args, **kwargs)


class CommandMixin:
    logger = logging.getLogger('CommandMixin')

    @property
    def command_name(self):
        return self.__class__.__module__.rsplit('.', 1).pop()

    def info(self, msg, *args):
        msg = '[%s] %s' % (self.command_name, msg % args)
        print(self.style.HTTP_INFO(msg))
        return self.logger.info(msg)

    def success(self, msg, *args):
        msg = '[%s] %s' % (self.command_name, msg % args)
        print(self.style.SUCCESS(msg))
        return self.logger.info(msg)

    def error(self, msg, *args):
        msg = '[%s] %s' % (self.command_name, msg % args)
        print(self.style.ERROR(msg))
        return self.logger.error(msg)

    def warn(self, msg, *args):
        msg = '[%s] %s' % (self.command_name, msg % args)
        print(self.style.WARNING(msg))
        return self.logger.warn(msg)

    def exception(self, e):
        return self.logger.exception(e)
