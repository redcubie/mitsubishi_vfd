
from enum import Enum, Flag


class MitsubishiVFD_OperationMode(Enum):
    NETWORK = 0
    EXTERNAL = 1
    PU = 2

class MitsubishiVFD_RunCommand(Flag):
    AUTOMATIC = 1 << 0
    FORWARD = 1 << 1
    REVERSE = 1 << 2
    SPEED_LOW = 1 << 3
    SPEED_MID = 1 << 4
    SPEED_HIGH = 1 << 5
    SECOND_FUNCTION_RT = 1 << 6
    MOTOR_STOP = 1 << 7

class MitsubishiVFD_RunCommandExtended(Flag):
    AUTOMATIC = 1 << 0
    FORWARD = 1 << 1
    REVERSE = 1 << 2
    SPEED_LOW = 1 << 3
    SPEED_MID = 1 << 4
    SPEED_HIGH = 1 << 5
    SECOND_FUNCTION_RT = 1 << 6
    MOTOR_STOP = 1 << 7
    JOG = 1 << 8
    AUTO_RESUME = 1 << 9
    STOP = 1 << 10
    RESET = 1 << 11
