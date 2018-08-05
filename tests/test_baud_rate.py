import typing
import unittest.mock as mock
import serial

import serialgsm


class FakeSerial(serial.SerialBase):
    def __init__(self, data: typing.List[bytes], **kwargs):
        self.count = 0
        self.data = data
        self.is_open = False

    def read(self, size=1):
        """\
        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """
        assert self.count < len(self.data)
        data = self.data[self.count]
        self.count += 1
        return data


def test_that_a_serial_connection_can_be_created():
    instance = serialgsm.establish_serial_connection(serial.serial_for_url("loop://"), serialgsm.BaudRate.RATE_9600)
    assert isinstance(instance, serial.SerialBase)


def test_that_a_serial_connection_can_be_created_with_auto_baud_detection(mocker):
    expected_baud_rate = serialgsm.BaudRate.RATE_57600

    serial_instance = serial.serial_for_url("loop://")
    mocker.patch('serialgsm.baudrate.determine_baud_rate', return_value=expected_baud_rate)
    serialgsm.establish_serial_connection(serial_instance)

    serialgsm.baudrate.determine_baud_rate.assert_called_with(serial_instance)
    assert expected_baud_rate == serial_instance.baudrate


def test_that_the_determine_baud_rate_tries_different_baud_rates():
    wrong = 'FOOBAR'.encode('UTF-8')
    okay = 'OK\r\n'.encode('UTF-8')
    fake_serial = FakeSerial([wrong, wrong, wrong, okay])
    magic_serial = mock.Mock(wraps=fake_serial)
    magic_serial.write = mock.MagicMock()

    assert serialgsm.BaudRate.RATE_19200 == serialgsm.determine_baud_rate(magic_serial)


def test_that_the_determine_baud_rate_returns_the_auto_rate_when_it_can_not_determine_the_baud_rate():
    wrong = 'FOOBAR'.encode('UTF-8')
    serial = FakeSerial([wrong] * (serialgsm.BaudRate.__len__() - 1))
    magic_serial = mock.Mock(wraps=serial)
    magic_serial.write = mock.MagicMock()

    assert serialgsm.BaudRate.RATE_AUTO == serialgsm.determine_baud_rate(magic_serial)
