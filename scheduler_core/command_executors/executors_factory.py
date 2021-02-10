import exceptions
from command_executors.command_executor import CommandExecutor
from command_executors.get_free_timetable_slots import GetFreeTimetableSlotsExecutor
from database.db import DB
from enums import CommandType


def create(command_type: CommandType, db: DB) -> CommandExecutor:
    """
    :raises:
        UnknownCommand если не найден исполнитель для команды данного типа
    """

    if command_type == CommandType.GET_FREE_TIMETABLE_SLOTS:
        return GetFreeTimetableSlotsExecutor(db)

    raise exceptions.UnknownCommand(f'Не найден исполнитель для команды данного типа: {command_type}')
