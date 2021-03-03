from typing import Dict

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.enums import CommandType


class DeleteServicesResponse(CommandResponse):
    def __str__(self):
        return f'DeleteServicesResponse(id={self.id}, status={self.status})'

    def get_command_type(self) -> CommandType:
        return CommandType.DELETE_SERVICES

    def _load_data(self, data: Dict) -> bool:
        return True

    def _unload_data(self) -> Dict:
        return {}
