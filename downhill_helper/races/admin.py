from django.contrib import admin

from races.models import RaceContestant, Race, RaceBracket, BracketContestant, RaceContestantQualification


class RaceAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True


class RaceContestantAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_display = ('id', 'race', 'name', 'best_qualification_time', 'helmet_number', 'qualification_number', 'is_open', 'is_amateur', 'is_master')
    list_editable = ('qualification_number', 'helmet_number')
    search_fields = ('name', 'helmet_number')
    list_filter = ('race__name', 'is_open', 'is_amateur', 'is_master')


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


admin.site.register(Race, RaceAdmin)
admin.site.register(RaceContestant, RaceContestantAdmin)
admin.site.register(RaceBracket, BracketAdmin)
admin.site.register(BracketContestant, BracketContestantAdmin)
admin.site.register(RaceContestantQualification, RaceContestantQualificationAdmin)
