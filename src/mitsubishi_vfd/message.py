
from .constants import *

STX = 0x02
ETX = 0x03
ENQ = 0x05
ACK = 0x06
NAK = 0x15

DEFAULT_WAITING_TIME = 0 // 10

def mitsubishivfd_calculate_checksum(data: bytes) -> bytes:
    return (sum(data) & 0xff).to_bytes().hex().upper().encode()

class MitsubishiVFDMessage:
    head_byte: int
    inverter_id: int
    has_checksum: bool

    def __init__(self, inverter_id: int, head: int = ENQ, has_checksum: bool = True) -> None:
        self.inverter_id = inverter_id
        assert 0 <= inverter_id and inverter_id <= 31
        self.head_byte = head
        self.has_checksum = has_checksum

    def to_bytes(self) -> bytes:
        out = bytearray(1)
        out[0] = self.head_byte
        content_bytes = self.content_to_bytes()
        out += content_bytes
        if self.has_checksum:
            checksum = mitsubishivfd_calculate_checksum(content_bytes)
            out += checksum

        return out

    def content_to_bytes(self):
        out = bytearray(2)
        out[0:2] = "{:02X}".format(self.inverter_id).encode()

        return out

    @classmethod
    def from_bytes(cls, data: bytes):
        raise NotImplementedError()


class MitsubishiVFDCommand(MitsubishiVFDMessage):
    instruction_code: int
    waiting_time: int | None
    def __init__(self, inverter_id: int, instruction_code: int, waiting_time: int | None = DEFAULT_WAITING_TIME) -> None:
        super().__init__(inverter_id, head=ENQ, has_checksum=True)
        self.instruction_code = instruction_code
        self.waiting_time = waiting_time

    def content_to_bytes(self):
        head = super().content_to_bytes()
        out = head + self.instruction_code.to_bytes(1, "big").hex().upper().encode()
        if self.waiting_time is not None:
            out += "{:01X}".format(self.waiting_time).encode()
        return out

class MitsubishiVFDCommand_WriteData(MitsubishiVFDCommand):
    data: int
    def __init__(self, inverter_id: int, instruction_code: int, data: int, waiting_time: int | None = DEFAULT_WAITING_TIME) -> None:
        super().__init__(inverter_id, instruction_code, waiting_time)
        self.data = data

class MitsubishiVFDCommand_WriteDataLong(MitsubishiVFDCommand_WriteData):
    def content_to_bytes(self):
        header = super().content_to_bytes()
        return header + self.data.to_bytes(2, "big").hex().upper().encode()

class MitsubishiVFDCommand_WriteDataShort(MitsubishiVFDCommand_WriteData):
    def content_to_bytes(self):
        header = super().content_to_bytes()
        return header + self.data.to_bytes(1, "big").hex().upper().encode()

class MitsubishiVFDCommand_ReadData(MitsubishiVFDCommand):
    pass



class MitsubishiVFDResponse(MitsubishiVFDMessage):
    pass

class MitsubishiVFDResponse_ACK(MitsubishiVFDResponse):
    def __init__(self, inverter_id: int) -> None:
        super().__init__(inverter_id, ACK, False)

class MitsubishiVFDResponse_NAK(MitsubishiVFDResponse):
    error_code: MitsubishiVFDCommError
    def __init__(self, inverter_id: int, error_code: MitsubishiVFDCommError) -> None:
        super().__init__(inverter_id, NAK, False)
        self.error_code = error_code

    def content_to_bytes(self):
        return super().content_to_bytes() + self.error_code.value.to_bytes(1).hex().upper().encode()

class MitsubishiVFDResponse_Data(MitsubishiVFDResponse):
    data: int
    def __init__(self, inverter_id: int, data: int) -> None:
        super().__init__(inverter_id, STX, True)
        self.data = data

class MitsubishiVFDResponse_DataLong(MitsubishiVFDResponse_Data):
    pass
class MitsubishiVFDResponse_DataShort(MitsubishiVFDResponse_Data):
    pass

MitsubishiVFDResponse_Any = MitsubishiVFDResponse_ACK | MitsubishiVFDResponse_NAK | MitsubishiVFDResponse_DataLong | MitsubishiVFDResponse_DataShort

import types
START_CHARS = types.SimpleNamespace()
START_CHARS.ACK = ACK
START_CHARS.NAK = NAK
START_CHARS.STX = STX


def parse_MitsubishiVFDResponse(data: bytes):
    assert len(data) >= 3
    inverter_id = int(data[1:1+2], 16)
    match data[0]:
        case START_CHARS.ACK:
            assert len(data) == 3
            return MitsubishiVFDResponse_ACK(inverter_id)

        case START_CHARS.NAK:
            # assuming inverter response
            assert len(data) == 4
            error_id = int(data[3:3+1], 16)
            error_obj = MitsubishiVFDCommError(error_id)

            return MitsubishiVFDResponse_NAK(inverter_id, error_obj)

        case START_CHARS.STX:
            assert len(data) >= 8
            if data[5] == ETX:
                dlen = 2
                assert len(data) == 8
            elif data[7] == ETX:
                dlen = 4
                assert len(data) == 10
            else:
                raise ValueError()
            payload_val = int(data[3:3+dlen], 16)
            checksum = data[3+dlen+1:]
            assert len(checksum) == 2
            assert checksum == mitsubishivfd_calculate_checksum(data[1:3+dlen])

            if dlen == 2:
                return MitsubishiVFDResponse_DataShort(inverter_id, payload_val)
            elif dlen == 4:
                return MitsubishiVFDResponse_DataLong(inverter_id, payload_val)
            else:
                assert False

        case _:
            raise ValueError()
