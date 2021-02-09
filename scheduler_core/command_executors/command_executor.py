from abc import ABC, abstractmethod

from commands.command import Command
from net import Client


class CommandExecutor(ABC):
    @abstractmethod
    async def execute(self, command: Command, client: Client) -> bool:
        pass
