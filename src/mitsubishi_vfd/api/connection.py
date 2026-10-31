
from ..raw.connection import MitsubishiVFDConnection
from ..raw.message import *
from ..raw.instructions import MitsubishiVFD_InstructionCode, MITSUBISHIVFD_PARAMETER_MASK_WRITE

from .constants import *

class MitsubishiVFD_APIConnection:
    conn: MitsubishiVFDConnection
    inverter_id: int
    def __init__(self, conn: MitsubishiVFDConnection, inverter_id: int) -> None:
        self.conn = conn
        self.inverter_id = inverter_id

    def set_frequency(self, frequency: float, save_to_eeprom = False):
        if frequency < 0 or frequency > 400:
            raise ValueError
        instruction_code = MitsubishiVFD_InstructionCode.FREQUENCY_SETPOINT_EEPROM_WRITE if save_to_eeprom \
            else MitsubishiVFD_InstructionCode.FREQUENCY_SETPOINT_RAM_WRITE
        value = int(frequency * 100)

        msg = MitsubishiVFDCommand_WriteDataLong(self.inverter_id, instruction_code.value, value)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)

    def get_frequency(self, from_eeprom = False) -> float:
        instruction_code = MitsubishiVFD_InstructionCode.FREQUENCY_SETPOINT_EEPROM_READ if from_eeprom \
            else MitsubishiVFD_InstructionCode.FREQUENCY_SETPOINT_RAM_READ
        msg = MitsubishiVFDCommand_ReadData(self.inverter_id, instruction_code.value)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)
        assert isinstance(res, MitsubishiVFDResponse_DataLong)

        return res.data / 100

    def set_runmode(self, command: MitsubishiVFD_RunCommand):
        instruction_code = MitsubishiVFD_InstructionCode.RUN_COMMAND
        msg = MitsubishiVFDCommand_WriteDataShort(self.inverter_id, instruction_code.value, command.value)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)
    
    def set_runmode_extended(self, command: MitsubishiVFD_RunCommandExtended):
        instruction_code = MitsubishiVFD_InstructionCode.RUN_COMMAND_EXTENDED
        msg = MitsubishiVFDCommand_WriteDataLong(self.inverter_id, instruction_code.value, command.value)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)


    def get_current_output_frequency_or_speed(self) -> float:
        instruction_code = MitsubishiVFD_InstructionCode.MONITOR_OUTPUT_FREQUENCY_SPEED
        msg = MitsubishiVFDCommand_ReadData(self.inverter_id, instruction_code.value)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)
        assert isinstance(res, MitsubishiVFDResponse_DataLong)

        return res.data / 100 # assuming frequency

    def get_current_output_current(self) -> float:
        instruction_code = MitsubishiVFD_InstructionCode.MONITOR_OUTPUT_CURRENT
        msg = MitsubishiVFDCommand_ReadData(self.inverter_id, instruction_code.value)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)
        assert isinstance(res, MitsubishiVFDResponse_DataLong)

        return res.data / 100 # assuming inverter <=55kW

    def get_current_output_voltage(self) -> float:
        instruction_code = MitsubishiVFD_InstructionCode.MONITOR_OUTPUT_VOLTAGE
        msg = MitsubishiVFDCommand_ReadData(self.inverter_id, instruction_code.value)
        res = self.conn.send_message(msg)
        assert isinstance(res, MitsubishiVFDResponse_DataLong)

        return res.data / 10

    def get_operation_mode(self) -> MitsubishiVFD_OperationMode:
        instruction_code = MitsubishiVFD_InstructionCode.OPERATION_MODE_READ
        msg = MitsubishiVFDCommand_ReadData(self.inverter_id, instruction_code.value)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)
        assert isinstance(res, MitsubishiVFDResponse_DataLong)
        return MitsubishiVFD_OperationMode(res.data)

    def set_operation_mode(self, mode: MitsubishiVFD_OperationMode):
        instruction_code = MitsubishiVFD_InstructionCode.OPERATION_MODE_WRITE
        msg = MitsubishiVFDCommand_WriteDataLong(self.inverter_id, instruction_code.value, mode.value)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)


    def get_parameter(self, parameter_id_obj: MitsubishiVFD_ParameterId | int) -> int:
        if isinstance(parameter_id_obj, MitsubishiVFD_ParameterId):
            parameter_id = parameter_id_obj.value
        else:
            parameter_id = parameter_id_obj

        if parameter_id >= 100 and parameter_id < 300:
            if parameter_id < 230:
                extension_number = 1
                effective_param_id = parameter_id - 160
            else:
                extension_number = 1
                effective_param_id = parameter_id - 192
        else:
            extension_number = parameter_id // 100
            effective_param_id = parameter_id % 100

        instruction_code = MitsubishiVFD_InstructionCode.PARAMETER_NUMBER_EXTENSION_WRITE
        msg = MitsubishiVFDCommand_WriteDataShort(self.inverter_id, instruction_code.value, extension_number)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)

        assert 0 <= effective_param_id and effective_param_id <= 0x63

        instruction_code = effective_param_id
        msg = MitsubishiVFDCommand_ReadData(self.inverter_id, instruction_code)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)
        assert isinstance(res, MitsubishiVFDResponse_DataLong)

        return res.data

    def set_parameter(self, parameter_id_obj: MitsubishiVFD_ParameterId | int, value: int):
        if isinstance(parameter_id_obj, MitsubishiVFD_ParameterId):
            parameter_id = parameter_id_obj.value
        else:
            parameter_id = parameter_id_obj

        if parameter_id >= 100 and parameter_id < 300:
            if parameter_id < 230:
                extension_number = 1
                effective_param_id = parameter_id - 160
            else:
                extension_number = 1
                effective_param_id = parameter_id - 192
        else:
            extension_number = parameter_id // 100
            effective_param_id = parameter_id % 100

        instruction_code = MitsubishiVFD_InstructionCode.PARAMETER_NUMBER_EXTENSION_WRITE
        msg = MitsubishiVFDCommand_WriteDataShort(self.inverter_id, instruction_code.value, extension_number)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)

        assert 0 <= effective_param_id and effective_param_id <= 0x63

        instruction_code = effective_param_id | MITSUBISHIVFD_PARAMETER_MASK_WRITE
        msg = MitsubishiVFDCommand_WriteDataLong(self.inverter_id, instruction_code, value)
        res = self.conn.send_message(msg)
        MitsubishiVFDResponse_raise_for_error(res)
