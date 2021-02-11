from command_responses.command_response import CommandResponse
from enums import CommandType


class AddServicesResponse(CommandResponse):
    def get_command_type(self) -> CommandType:
        return CommandType.ADD_SERVICES
