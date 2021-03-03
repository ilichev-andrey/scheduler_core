from typing import Dict

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.enums import CommandType


class AddServicesResponse(CommandResponse):
    def __str__(self):
        return f'AddServicesResponse(id={self.id}, status={self.status})'

    def get_command_type(self) -> CommandType:
        return CommandType.ADD_SERVICES

    def _load_data(self, data: Dict) -> bool:
        return True

    def _unload_data(self) -> Dict:
        return {}
