#!/usr/bin/env python3

import serial
from mitsubishi_vfd.raw.connection import MitsubishiVFDConnection
import time
from mitsubishi_vfd.api.connection import *

SERIAL_PORT = "/dev/ttyUSB0"
SERIAL_SPEED = 19200
INVERTER_ID = 1

ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED, 8, "E", 2, timeout=1, write_timeout=1)
raw_connection = MitsubishiVFDConnection(ser)
inv = MitsubishiVFD_APIConnection(raw_connection, INVERTER_ID)

def get_param(num: int):
    print(f"Param {num:03} is {inv.get_parameter(num)}")

# make sure we are in network mode (gives error if not)
inv.set_operation_mode(MitsubishiVFD_OperationMode.NETWORK)

# param 342 = 1 means that parameter writes will only be stored into RAM (cleared on power cycle)
inv.set_parameter(342, 1)

time.sleep(1)

inv.set_frequency(10.0)
inv.set_runmode_extended(MitsubishiVFD_RunCommandExtended.FORWARD)

time.sleep(10)
inv.set_runmode_extended(MitsubishiVFD_RunCommandExtended.MOTOR_STOP)

