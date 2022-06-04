from django.contrib import admin

from races.models import RaceContestant, Race


class RaceAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    # list_fields = (,)


class RaceContestantAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    # list_fields = (,)


admin.site.register(Race, RaceAdmin)
admin.site.register(RaceContestant, RaceContestantAdmin)
