import abc
import time
import typing
import serial


class SerialGSM(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, serial_connection: serial.Serial):
        self.serial_connection = serial_connection
        self.connected = False

    @abc.abstractmethod
    def get_imei(self):
        pass

    @abc.abstractmethod
    def send_sms(self, recipient: str, message: str):
        pass

    def send_at_command(self, command: str) -> typing.List[str]:
        self.check_online()
        full_command = "AT+{command}".format(command=command)

        return self.send_command(full_command)

    def send_command(self, command: str, filter_ok: bool = True) -> typing.List[str]:
        full_command = (command+"\r\n").encode()
        self.serial_connection.write(full_command)
        time.sleep(2)
        data = self.serial_connection.read_all()
        print(data)

        to_filter = [""]
        if filter_ok:
            to_filter.append("OK")

        decoded_parts = data.decode().strip().splitlines()
        decoded_parts = [p for p in decoded_parts if p not in to_filter]

        if len(decoded_parts) == 0:
            # TODO: raise error
            return ""

        return decoded_parts if len(decoded_parts) > 1 else decoded_parts[0]

    def check_online(self):
        if not self.connected:
            self.set_echo(False)
            value = self.send_command("AT", False)
            if value == "OK":
                print("We're connected!")
                self.connected = True

    def set_echo(self, enable: bool):
        self.serial_connection.write("ATE{state}\r\n".format(state=(0 if not enable else 1)).encode())

    def send_message_data(self, message: str):
        self.serial_connection.write((message + '\x1A\r\n').encode())
        time.sleep(2)
        data = self.serial_connection.read_all()
        print(data)
