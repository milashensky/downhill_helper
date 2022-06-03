import logging

from common.mixins import SerializedView, CsrfExemptMixin
from sensors.models import SensorSignal

logger = logging.getLogger(__name__)


class SensorSignalApi(CsrfExemptMixin, SerializedView):
    fields = ('id', 'sensor_mark', 'signal_registered_at', 'created_at')

    def get(self, request):
        signals = SensorSignal.objects.all()
        return signals

    def post(self, request):
        signal = SensorSignal.objects.create(**self.data)
        return signal
