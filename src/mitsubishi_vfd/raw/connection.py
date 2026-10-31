
from serial import Serial
from .message import MitsubishiVFDMessage, MitsubishiVFDResponse_Any, parse_MitsubishiVFDResponse

class MitsubishiVFDConnection:
    _ser: Serial
    _waiting_time: int | None
    _end_character: bytes

    def __init__(self, ser: Serial, waiting_time: int | None = 0, end_character = b"\r") -> None:
        self._ser = ser
        self._waiting_time = waiting_time
        if end_character not in (b"\r", b"\r\n"):
            raise ValueError()
        self._end_character = end_character

    def send_message(self, msg: MitsubishiVFDMessage) -> MitsubishiVFDResponse_Any:
        msg_bytes = msg.to_bytes()
        self._ser.write(msg_bytes+self._end_character)

        if self._end_character is not None:
            resp_bytes = self._ser.read_until(self._end_character)
        else:
            raise NotImplementedError()

        assert resp_bytes.endswith(self._end_character)

        return parse_MitsubishiVFDResponse(resp_bytes.removesuffix(self._end_character))
