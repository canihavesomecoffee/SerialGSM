import aenum
import serial


class BaudRate(aenum.IntEnum):
    RATE_AUTO = 0
    RATE_2400 = 2400
    RATE_4800 = 4800
    RATE_9600 = 9600
    RATE_19200 = 19200
    RATE_38400 = 38400
    RATE_57600 = 57600
    RATE_115200 = 115200


def determine_baud_rate(serial_instance: serial.Serial) -> BaudRate:
    for baud_rate in filter(lambda b: b != BaudRate.RATE_AUTO, BaudRate.__reversed__()):
        print("Trying to connect using baud rate {baud}".format(baud=baud_rate))
        serial_instance.baudrate = baud_rate
        serial_instance.write("AT\r\n".encode("UTF-8"))
        rcv = serial_instance.read(10)
        print("Received... {data}".format(data=rcv))
        if "OK\r\n" in rcv.decode():
            print("Received OK... We can communicate on this length")
            return baud_rate

    # TODO: raise exception instead.
    print("Failed to retrieve the baud rate!")
    return BaudRate.RATE_AUTO


def establish_serial_connection(
        serial_instance: serial.Serial, baud_rate: BaudRate = BaudRate.RATE_AUTO) -> serial.Serial:
    rate = baud_rate
    if baud_rate == BaudRate.RATE_AUTO:
        rate = determine_baud_rate(serial_instance)

    serial_instance.baudrate = rate
    return serial_instance
