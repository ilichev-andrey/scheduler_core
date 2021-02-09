import exceptions
from command_executors.command_executor import CommandExecutor
from enums import CommandType


def create(command_type: CommandType) -> CommandExecutor:
    """
    :raises:
        UnknownCommand если не найден исполнитель для команды данного типа
    """

    raise exceptions.UnknownCommand(f'Не найден исполнитель для команды данного типа: {command_type}')
