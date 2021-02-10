from abc import ABC, abstractmethod

from command_responses.command_response import CommandResponse
from commands.command import Command


class CommandExecutor(ABC):
    @abstractmethod
    async def execute(self, command: Command) -> CommandResponse:
        pass
