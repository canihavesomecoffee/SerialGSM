import serial

import serialgsm


def test_that_a_serial_gsm_instance_can_be_created_with_a_supported_model():
    instance = serialgsm.create_serial_gsm(serialgsm.Model.SIM900, serial.Serial())
    assert isinstance(instance, serialgsm.SerialGSM)
