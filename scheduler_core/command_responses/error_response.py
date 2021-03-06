from typing import Dict

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.enums import CommandType, CommandStatus


class ErrorResponse(CommandResponse):
    command_type = CommandType

    def __init__(self, command_id: str = None, command_type: CommandType = None):
        super().__init__(command_id=command_id, status=CommandStatus.INTERNAL_ERROR)
        if command_type is None:
            command_type = CommandType.UNKNOWN

        self.command_type = command_type

    def __str__(self):
        return f'ErrorResponse(id={self.id}, status={self.status}, command_type={self.command_type})'

    def get_command_type(self) -> CommandType:
        return self.command_type

    def _load_data(self, data: Dict) -> bool:
        return False

    def _unload_data(self) -> Dict:
        return {}
