
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
    def from_bytes(cls: "MitsubishiVFDMessage", data: bytes):
        inst = cls()

        head = data[0]
        assert head in [ENQ, STX, ACK, NAK]

        station_number = int(data[1:2].decode(), 16)

        return inst


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


class MitsubishiVFDResponse():
    pass
