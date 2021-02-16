from scheduler_core.commands.command import Command
from scheduler_core.enums import CommandType


class GetServicesCommand(Command):
    def get_type(self) -> CommandType:
        return CommandType.GET_SERVICES
