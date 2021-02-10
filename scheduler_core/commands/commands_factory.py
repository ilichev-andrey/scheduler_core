import exceptions
from commands.command import Command
from commands.get_free_timetable_slots import GetFreeTimetableSlotsCommand
from commands.get_workers import GetWorkersCommand
from enums import CommandType


def create(command_type: CommandType) -> Command:
    """
    :raises:
        UnknownCommand если команда данного типа не поддерживается
    """

    if command_type == CommandType.GET_FREE_TIMETABLE_SLOTS:
        return GetFreeTimetableSlotsCommand()
    if command_type == CommandType.GET_WORKERS:
        return GetWorkersCommand()

    raise exceptions.UnknownCommand(f'Не поддерживается команда данного типа: {command_type}')
