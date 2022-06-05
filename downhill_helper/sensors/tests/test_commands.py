import freezegun

from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from django.utils import timezone

from sensors.management.commands import track_start_finish


class NormalizeBookTitlesSimpleTests(SimpleTestCase):

    def patch_rpi(self):
        MockRPi = MagicMock()
        self.GPIO_mock = MockRPi.GPIO
        modules = {
            'RPi': MockRPi,
            'RPi.GPIO': self.GPIO_mock,
        }
        patcher = patch.dict('sys.modules', modules)
        patcher.start()

    def test_handle_sensor(self):
        with patch('sensors.management.commands.track_start_finish.send_signal_request') as send_signal_request_mock:
            serial_mock = MagicMock()
            serial_mock.readline = MagicMock(return_value=b'1\r\n')
            command = track_start_finish.Command()
            command.connection = serial_mock
            command.race_id = 1
            with freezegun.freeze_time('2020-01-02 00:00:00') as last_signal_time:
                command.last_signal_time = last_signal_time
                command.handle_sensor('start', False)
                send_signal_request_mock.assert_called_with(timezone.now(), 'start', 1)
            send_signal_request_mock.reset_mock()

            serial_mock.readline = MagicMock(return_value=b'')
            with freezegun.freeze_time('2020-01-02 00:00:01'):
                command.handle_sensor('start', False)
                # not faded yet
                send_signal_request_mock.assert_not_called()

            with freezegun.freeze_time('2020-01-02 00:00:20'):
                command.handle_sensor('start', False)
                # faded but no signal since no sensor value
                send_signal_request_mock.assert_not_called()

            with freezegun.freeze_time('2020-01-02 00:00:30'):
                command.handle_sensor('start', False)
                # no signal
                send_signal_request_mock.assert_not_called()

            serial_mock.readline = MagicMock(return_value=b'1\r\n')
            with freezegun.freeze_time('2020-01-02 00:00:40'):
                command.handle_sensor('start', False)
                # signal
                send_signal_request_mock.assert_called_with(timezone.now(), 'start', 1)
            send_signal_request_mock.reset_mock()

            with freezegun.freeze_time('2020-01-02 00:01:00'):
                command.handle_sensor('start', False)
                # no signal bc signal is not faded
                send_signal_request_mock.assert_not_called()

            with freezegun.freeze_time('2020-01-02 00:01:20'):
                command.handle_sensor('start', False)
                # no signal bc signal is not faded
                send_signal_request_mock.assert_not_called()

    def test_handle_sensor_native(self):
        self.patch_rpi()
        self.GPIO_mock.HIGH = 1
        self.GPIO_mock.input = MagicMock(return_value=self.GPIO_mock.HIGH)
        with patch('sensors.management.commands.track_start_finish.send_signal_request') as send_signal_request_mock:
            command = track_start_finish.Command()
            command.connection = 3
            command.race_id = 1
            with freezegun.freeze_time('2020-01-02 00:00:00') as last_signal_time:
                command.last_signal_time = last_signal_time
                command.handle_sensor('start', True)
                send_signal_request_mock.assert_called_with(timezone.now(), 'start', 1)
            send_signal_request_mock.reset_mock()

            self.GPIO_mock.input = MagicMock(return_value=0)
            with freezegun.freeze_time('2020-01-02 00:00:01'):
                command.handle_sensor('start', True)
                # not faded yet
                send_signal_request_mock.assert_not_called()

    def test_setup_port(self):
        with patch('serial.Serial', MagicMock(return_value='Mock')) as serial_mock:
            result = track_start_finish.setup_port('port1', False)
            serial_mock.assert_called_with('port1', 9600, timeout=1)
            self.assertEqual(result, 'Mock')
        # native
        self.patch_rpi()
        self.GPIO_mock.BOARD = 'BOARD'
        self.GPIO_mock.IN = 'IN'
        self.GPIO_mock.setmode = MagicMock()
        self.GPIO_mock.setup = MagicMock()
        result = track_start_finish.setup_port('3', True)
        self.assertEqual(result, 3)
        self.GPIO_mock.setmode.assert_called_with(self.GPIO_mock.BOARD)
        self.GPIO_mock.setup.assert_called_with(3, self.GPIO_mock.IN)

    def test_close_port(self):
        serial_mock = MagicMock()
        serial_mock.close = MagicMock()
        track_start_finish.close_port(serial_mock, False)
        serial_mock.close.assert_called()
        # native
        self.patch_rpi()
        self.GPIO_mock.cleanup = MagicMock()
        track_start_finish.close_port(0, True)
        self.GPIO_mock.cleanup.assert_called()

    def test_read_port(self):
        serial_mock = MagicMock()
        serial_mock.readline = MagicMock(return_value=b'1/r/n')
        result = track_start_finish.read_port(serial_mock, False)
        self.assertEqual(result, True)
        # native
        self.patch_rpi()
        self.GPIO_mock.HIGH = 1
        self.GPIO_mock.input = MagicMock(return_value=self.GPIO_mock.HIGH)
        result = track_start_finish.read_port(3, True)
        self.assertEqual(result, True)
        self.GPIO_mock.input.assert_called_with(3)
