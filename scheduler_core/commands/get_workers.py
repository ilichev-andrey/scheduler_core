from scheduler_core.commands.command import Command
from scheduler_core.enums import CommandType


class GetWorkersCommand(Command):
    def get_type(self) -> CommandType:
        return CommandType.GET_WORKERS
