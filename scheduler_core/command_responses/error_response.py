from command_responses.command_response import CommandResponse
from enums import CommandType, CommandStatus


class ErrorResponse(CommandResponse):
    command_type = CommandType

    def __init__(self, command_id: str = None, command_type: CommandType = None):
        super().__init__(command_id=command_id, status=CommandStatus.INTERNAL_ERROR)
        if command_type is None:
            command_type = CommandType.UNKNOWN

        self.command_type = command_type

    def get_command_type(self) -> CommandType:
        return self.command_type
