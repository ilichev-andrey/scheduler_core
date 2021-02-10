import exceptions
from commands.command import Command
from commands.get_free_timetable_slots import GetFreeTimetableSlotsCommand
from enums import CommandType


def create(command_type: CommandType) -> Command:
    """
    :raises:
        UnknownCommand если команда данного типа не поддерживается
    """

    if command_type == CommandType.GET_FREE_TIMETABLE_SLOTS:
        return GetFreeTimetableSlotsCommand()

    raise exceptions.UnknownCommand(f'Не поддерживается команда данного типа: {command_type}')
