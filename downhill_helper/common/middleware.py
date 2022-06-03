import logging

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class DebugToolBarMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if "dtb" in request.GET:
            if not getattr(settings, "DEBUG_TOOLBAR", None):
                return HttpResponse(
                    'Please add in your "local_settings.py": <pre><code>DEBUG_TOOLBAR = True</code></pre>'
                )
            return HttpResponse(
                '<html><head><meta charset="utf-8"></head><body>%s</body></html>'
                % response.content.decode()
            )
        return response
