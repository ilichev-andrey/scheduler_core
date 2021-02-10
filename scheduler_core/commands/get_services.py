from commands.command import Command
from enums import CommandType


class GetServicesCommand(Command):
    def get_type(self) -> CommandType:
        return CommandType.GET_SERVICES
