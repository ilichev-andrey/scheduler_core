from abc import ABC, abstractmethod

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.commands.command import Command


class CommandExecutor(ABC):
    @abstractmethod
    async def execute(self, command: Command) -> CommandResponse:
        pass
