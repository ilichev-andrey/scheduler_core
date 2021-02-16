from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.enums import CommandType


class AddUserResponse(CommandResponse):
    def get_command_type(self) -> CommandType:
        return CommandType.ADD_USER
