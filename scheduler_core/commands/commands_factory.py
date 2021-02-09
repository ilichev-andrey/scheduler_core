import exceptions
from commands.command import Command
from enums import CommandType


def create(command_type: CommandType) -> Command:
    """
    :raises:
        UnknownCommand если команда данного типа не поддерживается
    """

    raise exceptions.UnknownCommand(f'Не поддерживается команда данного типа: {command_type}')
