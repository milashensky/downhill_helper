import serial
import logging
import requests
import threading

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)

SIGNAL_FADE_SECONDS = 10


def send_signal_request(time, mark, race_id, retries=0):
    if retries > settings.MAX_SEND_SIGNAL_RERIES:
        print(f'too much retries for time "{time}", quiting')
        return
    endpoint = reverse('sensors:signal_api')
    url = f'{settings.SENSOR_BACKEND_HOST}{endpoint}'
    data = {
        'signal_registered_at': str(time),
        'sensor_mark': mark,
        'race_id': int(race_id),
    }

    try:
        requests.post(url, json=data)
        print(f'signal with time "{time}" has been successfuly sent')
    except Exception as e:
        print('error "%s", retrying' % e)
        retries += 1
        send_signal_request(time, mark, race_id, retries)


def setup_port(port, is_native):
    """Sets up the port (serial or native) to read and returns connection info.
    Serial mode will return the serial.connection object
    Native pin will just return the pin number.
    """
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
    """Closes the connection with port.
    """
    # pin
    if is_native:
        import RPi.GPIO as GPIO

        GPIO.cleanup()
        return
    # serial
    connection.close()


def read_port(connection, is_native):
    """Reads the port and returns `True` if sensor sending any data.
    """
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
    help = 'Tracks a signal of start or finish from the sensor and sends it to the backend'
    last_signal_time = timezone.now()
    connection = None
    has_signal = False

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('-n', '--native', dest='is_native', action='store_true', default=False, help='Is native pin used (or True), or should use serial')
        parser.add_argument('-t', '--test', dest='is_test', action='store_true', default=False, help='A flag to test the sensor connection, without sending the data')
        parser.add_argument('-p', '--port', dest='port', default='/dev/ttyACM0', help='GPIO board pin (if set up as native) or serial port number')
        parser.add_argument('-m', '--mark', dest='mark', default='start', help='Sensor mark, start or finish')
        parser.add_argument('-r', '--race_id', dest='race_id', type=int, required=True, help='ID of the race, to attach the signal')

    def handle(self, is_native, port, mark, is_test, race_id, *args, **options):
        self.race_id = race_id
        print('Started registring start-finish. Sensor is set up as: "%s"' % mark)
        if is_test:
            print('Running in the test mode')
        running = True
        self.connection = setup_port(port, is_native)
        while running:
            try:
                self.handle_sensor(mark, is_native, is_test)
            except KeyboardInterrupt:
                running = False
        close_port(self.connection, is_native)
        print('Registring start-finish is Done')

    def handle_sensor(self, mark, is_native, is_test=False):
        is_signal_recieved = read_port(self.connection, is_native)
        if not self.has_signal and is_signal_recieved:
            self.last_signal_time = timezone.now()
            self.has_signal = True
            print('Catched signal at "%s", sending' % self.last_signal_time)
            if is_test:
                print('sending is skipped, since test mode is on')
            else:
                thread = threading.Thread(
                    target=send_signal_request,
                    kwargs={
                        'time': self.last_signal_time,
                        'mark': mark,
                        'race_id': self.race_id,
                    },
                    daemon=True,
                )
                thread.start()
                print('sending')
        # debouncing
        time_delta = timezone.now() - self.last_signal_time
        if self.has_signal and time_delta.total_seconds() > SIGNAL_FADE_SECONDS and not is_signal_recieved:
            self.has_signal = False
            print('Ok, faded')
