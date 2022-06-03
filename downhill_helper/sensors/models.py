from django.db import models


class SensorSignal(models.Model):
    sensor_mark = models.CharField(max_length=32)
    signal_registered_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sensor_mark} at {self.signal_registered_at}'
