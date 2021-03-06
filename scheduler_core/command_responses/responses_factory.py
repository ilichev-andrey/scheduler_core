from scheduler_core import exceptions
from scheduler_core.command_responses.add_services import AddServicesResponse
from scheduler_core.command_responses.add_timetable_slots import AddTimetableSlotsResponse
from scheduler_core.command_responses.add_user import AddUserResponse
from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.command_responses.delete_services import DeleteServicesResponse
from scheduler_core.command_responses.get_client_timetable import GetClientTimetableResponse
from scheduler_core.command_responses.get_free_timetable_slots import GetFreeTimetableSlotsResponse
from scheduler_core.command_responses.get_services import GetServicesResponse
from scheduler_core.command_responses.get_user import GetUserResponse
from scheduler_core.command_responses.get_worker_timetable import GetWorkerTimetableResponse
from scheduler_core.command_responses.get_workers import GetWorkersResponse
from scheduler_core.command_responses.release_timetable_slot import ReleaseTimetableSlotsResponse
from scheduler_core.command_responses.take_timetable_slots import TakeTimetableSlotsResponse
from scheduler_core.command_responses.update_user import UpdateUserResponse
from scheduler_core.enums import CommandType


def create(command_type: CommandType) -> CommandResponse:
    """
    :raises:
        UnknownCommand если команда данного типа не поддерживается
    """

    if command_type == CommandType.GET_FREE_TIMETABLE_SLOTS:
        return GetFreeTimetableSlotsResponse()
    if command_type == CommandType.GET_WORKERS:
        return GetWorkersResponse()
    if command_type == CommandType.GET_SERVICES:
        return GetServicesResponse()
    if command_type == CommandType.ADD_SERVICES:
        return AddServicesResponse()
    if command_type == CommandType.ADD_USER:
        return AddUserResponse()
    if command_type == CommandType.GET_USER:
        return GetUserResponse()
    if command_type == CommandType.TAKE_TIMETABLE_SLOTS:
        return TakeTimetableSlotsResponse()
    if command_type == CommandType.GET_CLIENT_TIMETABLE:
        return GetClientTimetableResponse()
    if command_type == CommandType.UPDATE_USER:
        return UpdateUserResponse()
    if command_type == CommandType.GET_WORKER_TIMETABLE:
        return GetWorkerTimetableResponse()
    if command_type == CommandType.DELETE_SERVICES:
        return DeleteServicesResponse()
    if command_type == CommandType.ADD_TIMETABLE_SLOTS:
        return AddTimetableSlotsResponse()
    if command_type == CommandType.RELEASE_TIMETABLE_SLOTS:
        return ReleaseTimetableSlotsResponse()

    raise exceptions.UnknownCommand(f'Не поддерживается команда данного типа: {command_type}')
