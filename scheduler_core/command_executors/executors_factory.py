from scheduler_core import exceptions
from scheduler_core.command_executors.add_services import AddServicesExecutor
from scheduler_core.command_executors.add_user import AddUserExecutor
from scheduler_core.command_executors.command_executor import CommandExecutor
from scheduler_core.command_executors.get_free_timetable_slots import GetFreeTimetableSlotsExecutor
from scheduler_core.command_executors.get_services import GetServicesExecutor
from scheduler_core.command_executors.get_user import GetUserExecutor
from scheduler_core.command_executors.get_workers import GetWorkersExecutor
from scheduler_core.command_executors.take_timetable_slots import TakeTimetableSlotsExecutor
from scheduler_core.database.db import DB
from scheduler_core.enums import CommandType


def create(command_type: CommandType, db: DB) -> CommandExecutor:
    """
    :raises:
        UnknownCommand если не найден исполнитель для команды данного типа
    """

    if command_type == CommandType.GET_FREE_TIMETABLE_SLOTS:
        return GetFreeTimetableSlotsExecutor(db)
    if command_type == CommandType.GET_WORKERS:
        return GetWorkersExecutor(db)
    if command_type == CommandType.GET_SERVICES:
        return GetServicesExecutor(db)
    if command_type == CommandType.ADD_SERVICES:
        return AddServicesExecutor(db)
    if command_type == CommandType.ADD_USER:
        return AddUserExecutor(db)
    if command_type == CommandType.GET_USER:
        return GetUserExecutor(db)
    if command_type == CommandType.TAKE_TIMETABLE_SLOTS:
        return TakeTimetableSlotsExecutor(db)

    raise exceptions.UnknownCommand(f'Не найден исполнитель для команды данного типа: {command_type}')
