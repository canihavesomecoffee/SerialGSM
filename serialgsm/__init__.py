import logging
import serial
import aenum

from .baudrate import BaudRate, determine_baud_rate, establish_serial_connection
from .gsm import SerialGSM
from .sim900 import SerialSIM900

name = "serialgsm"

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())


class Model(aenum.Enum):
    SIM900 = aenum.auto()


def create_serial_gsm(model: Model, serial_instance: serial.Serial) -> SerialGSM:
    if model == Model.SIM900:
        instance = SerialSIM900(serial_instance)
    else:
        raise ValueError("Unsupported model")
    return instance
