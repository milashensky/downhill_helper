from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from races.models import RaceContestant, Race, RaceBracket, BracketContestant, RaceContestantQualification
from races.utils import set_qualification_time_by_sensors_data, create_initial_brackets, create_stage_brackets


def assign_qualification_time(modeladmin, request, queryset):
    for contestant in queryset:
        result = set_qualification_time_by_sensors_data(contestant)
        if result:
            messages.success(request, f'assigned "{result}" to "{contestant}"')
        else:
            messages.error(request, f'could not assign last sensor time to "{contestant}"')


def create_initial_brackets(modeladmin, request, queryset):
    race = queryset.first()
    url = reverse('admin:create_initial_brackets_view', kwargs={'race_id': race.id})
    return HttpResponseRedirect(url)


def create_stage_brackets(modeladmin, request, queryset):
    race = queryset.first()
    url = reverse('admin:create_stage_brackets_view', kwargs={'race_id': race.id})
    return HttpResponseRedirect(url)


class RaceAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    actions = (create_initial_brackets, create_stage_brackets)


class RaceContestantAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_display = ('id', 'race', 'name', 'best_qualification_time', 'helmet_number', 'qualification_number', 'is_open', 'is_amateur', 'is_master')
    list_editable = ('qualification_number', 'helmet_number')
    search_fields = ('name', 'helmet_number')
    list_filter = ('race__name', 'is_open', 'is_amateur', 'is_master')
    actions = (assign_qualification_time,)


class BracketAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_filter = ('race__name', 'level', 'type')


class BracketContestantAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_display = ('bracket', 'contestant_name', 'qualification_number', 'helmet_number', 'position', 'finished_at')
    list_editable = ('position',)
    list_filter = ('contestant__race__name', 'bracket__level', 'bracket__id', 'bracket__type')


class RaceContestantQualificationAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_display = ('id', 'race', 'contestant_name', 'qualification_time')
    list_filter = ('contestant__race__name',)


# def get_admin_urls(default_handler):
#     def get_urls():
#         my_urls = [
#
#         ]
#         return my_urls + default_handler()
#     return get_urls
#
#
# get_urls_default = admin.site.get_urls
# admin.site.get_urls = get_admin_urls(get_urls_default)
admin.site.register(Race, RaceAdmin)
admin.site.register(RaceContestant, RaceContestantAdmin)
admin.site.register(RaceBracket, BracketAdmin)
admin.site.register(BracketContestant, BracketContestantAdmin)
admin.site.register(RaceContestantQualification, RaceContestantQualificationAdmin)
