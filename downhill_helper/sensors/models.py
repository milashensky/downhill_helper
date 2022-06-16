from django.db import models
from races.models import RaceContestantQualification, Race

START_SENSOR_MARK = 'start'
FINISH_SENSOR_MARK = 'finish'

SENSOR_MARKS = (
    (START_SENSOR_MARK, START_SENSOR_MARK),
    (FINISH_SENSOR_MARK, FINISH_SENSOR_MARK),
)


class SensorSignal(models.Model):
    race = models.ForeignKey(Race, related_name='signals', on_delete=models.CASCADE)
    sensor_mark = models.CharField(max_length=32, choices=SENSOR_MARKS)
    signal_registered_at = models.DateTimeField()
    contestant = models.ForeignKey(RaceContestantQualification, null=True, blank=True, related_name='signals', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sensor_mark} at {self.signal_registered_at}'
