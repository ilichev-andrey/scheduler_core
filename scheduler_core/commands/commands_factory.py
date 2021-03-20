from scheduler_core import exceptions
from scheduler_core.commands.add_services import AddServicesCommand
from scheduler_core.commands.add_timetable_slots import AddTimetableSlotsCommand
from scheduler_core.commands.add_user import AddUserCommand
from scheduler_core.commands.command import Command
from scheduler_core.commands.delete_services import DeleteServicesCommand
from scheduler_core.commands.get_client_timetable import GetClientTimetableCommand
from scheduler_core.commands.get_free_timetable_slots import GetFreeTimetableSlotsCommand
from scheduler_core.commands.get_services import GetServicesCommand
from scheduler_core.commands.get_user import GetUserCommand
from scheduler_core.commands.get_worker_timetable import GetWorkerTimetableCommand
from scheduler_core.commands.get_workers import GetWorkersCommand
from scheduler_core.commands.release_timetable_slot import ReleaseTimetableSlotsCommand
from scheduler_core.commands.take_timetable_slots import TakeTimetableSlotsCommand
from scheduler_core.commands.update_user import UpdateUserCommand
from scheduler_core.enums import CommandType


def create(command_type: CommandType) -> Command:
    """
    :raises:
        UnknownCommand если команда данного типа не поддерживается
    """

    if command_type == CommandType.GET_FREE_TIMETABLE_SLOTS:
        return GetFreeTimetableSlotsCommand()
    if command_type == CommandType.GET_WORKERS:
        return GetWorkersCommand()
    if command_type == CommandType.GET_SERVICES:
        return GetServicesCommand()
    if command_type == CommandType.ADD_SERVICES:
        return AddServicesCommand()
    if command_type == CommandType.ADD_USER:
        return AddUserCommand()
    if command_type == CommandType.GET_USER:
        return GetUserCommand()
    if command_type == CommandType.TAKE_TIMETABLE_SLOTS:
        return TakeTimetableSlotsCommand()
    if command_type == CommandType.GET_CLIENT_TIMETABLE:
        return GetClientTimetableCommand()
    if command_type == CommandType.UPDATE_USER:
        return UpdateUserCommand()
    if command_type == CommandType.GET_WORKER_TIMETABLE:
        return GetWorkerTimetableCommand()
    if command_type == CommandType.DELETE_SERVICES:
        return DeleteServicesCommand()
    if command_type == CommandType.ADD_TIMETABLE_SLOTS:
        return AddTimetableSlotsCommand()
    if command_type == CommandType.RELEASE_TIMETABLE_SLOTS:
        return ReleaseTimetableSlotsCommand()

    raise exceptions.UnknownCommand(f'Не поддерживается команда данного типа: {command_type}')
