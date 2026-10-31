from .raw.constants import MitsubishiVFDCommError

class MitsubishiVFD_Communication_BaseError(Exception):
    pass

class MitsubishiVFD_Communication_ComputerNakError(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_ParityError(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_SumCheckError(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_ProtocolError(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_FramingError(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_OverrunError(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_UndefinedError6(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_CharacterError(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_UndefinedError8(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_UndefinedError9(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_ModeError(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_InstructionError(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_DataRangeError(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_UndefinedErrorD(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_UndefinedErrorE(MitsubishiVFD_Communication_BaseError):
    pass
class MitsubishiVFD_Communication_UndefinedErrorF(MitsubishiVFD_Communication_BaseError):
    pass

def MitsubishiVFD_Communication_get_error(error_type: MitsubishiVFDCommError) -> MitsubishiVFD_Communication_BaseError:
    args = ()
    match error_type:
        case MitsubishiVFDCommError.COMPUTER_NAK_ERROR:
            return MitsubishiVFD_Communication_ComputerNakError(*args)
        case MitsubishiVFDCommError.PARITY_ERROR:
            return MitsubishiVFD_Communication_ParityError(*args)
        case MitsubishiVFDCommError.SUM_CHECK_ERROR:
            return MitsubishiVFD_Communication_SumCheckError(*args)
        case MitsubishiVFDCommError.PROTOCOL_ERROR:
            return MitsubishiVFD_Communication_ProtocolError(*args)
        case MitsubishiVFDCommError.FRAMING_ERROR:
            return MitsubishiVFD_Communication_FramingError(*args)
        case MitsubishiVFDCommError.OVERRUN_ERROR:
            return MitsubishiVFD_Communication_OverrunError(*args)
        case MitsubishiVFDCommError.UNDEFINED_ERROR_6:
            return MitsubishiVFD_Communication_UndefinedError6(*args)
        case MitsubishiVFDCommError.CHARACTER_ERROR:
            return MitsubishiVFD_Communication_CharacterError(*args)
        case MitsubishiVFDCommError.UNDEFINED_ERROR_8:
            return MitsubishiVFD_Communication_UndefinedError8(*args)
        case MitsubishiVFDCommError.UNDEFINED_ERROR_9:
            return MitsubishiVFD_Communication_UndefinedError9(*args)
        case MitsubishiVFDCommError.MODE_ERROR:
            return MitsubishiVFD_Communication_ModeError(*args)
        case MitsubishiVFDCommError.INSTRUCTION_ERROR:
            return MitsubishiVFD_Communication_InstructionError(*args)
        case MitsubishiVFDCommError.DATA_RANGE_ERROR:
            return MitsubishiVFD_Communication_DataRangeError(*args)
        case MitsubishiVFDCommError.UNDEFINED_ERROR_D:
            return MitsubishiVFD_Communication_UndefinedErrorD(*args)
        case MitsubishiVFDCommError.UNDEFINED_ERROR_E:
            return MitsubishiVFD_Communication_UndefinedErrorE(*args)
        case MitsubishiVFDCommError.UNDEFINED_ERROR_F:
            return MitsubishiVFD_Communication_UndefinedErrorF(*args)
