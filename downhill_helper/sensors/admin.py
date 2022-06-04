from django.contrib import admin

from sensors.models import SensorSignal


class SensorSignalAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_display = ('id', 'sensor_mark', 'signal_registered_at', 'created_at')


admin.site.register(SensorSignal, SensorSignalAdmin)
