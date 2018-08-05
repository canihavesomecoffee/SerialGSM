from serial import Serial

import serialgsm

if __name__ == "__main__":
    # You can directly create a serial connection, but you can also use the auto-baud feature to let the library decide
    # the baud rate.
    port = "/dev/serial0"
    baud_rate = serialgsm.BaudRate.RATE_9600

    serial = Serial(port)
    # serial = Serial(port, baud_rate.value)  # Create your own serial. In this case you don't need the line below.

    serialgsm.establish_serial_connection(serial, baud_rate)  # Establish with fixed baud-rate
    # establish_serial_connection(serial)  # Use the auto-baud feature

    api = serialgsm.create_serial_gsm(serialgsm.Model.SIM900, serial)

    api.send_sms("+32123123123", "Hello world")
