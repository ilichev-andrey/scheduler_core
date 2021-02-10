from commands.command import Command
from enums import CommandType


class GetWorkersCommand(Command):
    def get_type(self) -> CommandType:
        return CommandType.GET_WORKERS
