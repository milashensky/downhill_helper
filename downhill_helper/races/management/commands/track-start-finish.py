import serial
import logging

from django.utils import timezone
from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)

SIGNAL_FADE_SECONDS = 10


def setup_port(port, is_native):
    # pin
    if is_native:
        import RPi.GPIO as GPIO

        port_number = int(port)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(port_number, GPIO.IN)
        return port_number
    # serial
    connection = serial.Serial(port, 9600, timeout=1)
    return connection


def close_port(connection, is_native):
    # pin
    if is_native:
        import RPi.GPIO as GPIO

        GPIO.cleanup()
        return
    # serial
    connection.close()


def read_port(connection, is_native):
    # pin
    if is_native:
        import RPi.GPIO as GPIO

        data = GPIO.input(connection)
        return data == GPIO.HIGH
    # serial
    data = connection.readline()
    is_signal_recieved = data.decode().startswith('1')
    return is_signal_recieved


class Command(BaseCommand):
    help = 'Tracks a signal of start or finish and sends it to the backend'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('-native', '--native', dest='is_native', action='store_true', default=False, help='Is native pin used (or True), or should use serial')
        parser.add_argument('-p', '--port', dest='port', default='/dev/ttyACM0', help='GPIO board pin (if set up as native) or serial port number')
        parser.add_argument('-m', '--mark', dest='mark', default='start', help='Sensor mark, start or finish')

    def handle(self, is_native, port, mark, *args, **options):
        print('Started registring start-finish. Sensor is set up as: "%s"' % mark)
        connection = setup_port(port, is_native)
        running = True
        has_signal = False
        last_signal_time = timezone.now()
        while running:
            try:
                is_signal_recieved = read_port(connection, is_native)
                if not has_signal and is_signal_recieved:
                    last_signal_time = timezone.now()
                    has_signal = True
                    print('Catched signal at "%s", sending' % last_signal_time)
                # debouncing
                time_delta = timezone.now() - last_signal_time
                if has_signal and time_delta.seconds > SIGNAL_FADE_SECONDS and not is_signal_recieved:
                    has_signal = False
                    print('Ok, faded')

            except KeyboardInterrupt:
                running = False
        close_port(connection, is_native)
        print('Registring start-finish is Done')
