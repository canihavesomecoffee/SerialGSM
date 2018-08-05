import serial

from .gsm import SerialGSM


class SerialSIM900(SerialGSM):
    def __init__(self, serial_connection: serial.Serial):
        super().__init__(serial_connection)

    def get_imei(self):
        return self.send_at_command("GSN")

    def send_sms(self, recipient: str, message: str):
        self.send_at_command('CMGS="{recipient}"'.format(recipient=recipient))
        self.send_message_data(message)

