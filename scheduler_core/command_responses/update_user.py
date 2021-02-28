from typing import Dict

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.enums import CommandType


class UpdateUserResponse(CommandResponse):
    def get_command_type(self) -> CommandType:
        return CommandType.UPDATE_USER

    def _load_data(self, data: Dict) -> bool:
        return True

    def _unload_data(self) -> Dict:
        return {}
