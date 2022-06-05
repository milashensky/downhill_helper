import json
from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

from races.models import Race
from sensors.models import START_SENSOR_MARK


class ApiTests(TestCase):

    def test_signal_api(self):
        race = Race.objects.create(name='speedy')
        url = reverse('sensors:signal_api')
        time = timezone.now()
        data = json.dumps({
            'signal_registered_at': str(time),
            'sensor_mark': START_SENSOR_MARK,
            'race_id': race.id,
        })
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        signals = race.signals.all()
        self.assertEqual(signals.count(), 1)
        signal = signals.first()
        self.assertEqual(signal.signal_registered_at, time)
        self.assertEqual(signal.sensor_mark, START_SENSOR_MARK)
