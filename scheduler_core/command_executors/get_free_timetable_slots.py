from datetime import timedelta
from typing import List

from command_executors.command_executor import CommandExecutor
from command_responses.command_response import CommandResponse
from command_responses.get_free_timetable_slots import GetFreeTimetableSlotsResponse
from commands.get_free_timetable_slots import GetFreeTimetableSlotsCommand
from database.containers import Service, TimetableEntry
from database.db import DB
from database.provider.service import ServiceProvider
from database.provider.timetable import TimetableProvider
from enums import CommandStatus
from wrappers import LoggerWrap


def _get_services_execution_time(services: List[Service]) -> int:
    execution_time_minutes = 0
    for service in services:
        execution_time_minutes += service.execution_time_minutes
    return execution_time_minutes


def _filter_slots_by_execution_time(slots: List[TimetableEntry], execution_time_minutes: int) -> List[TimetableEntry]:
    slots.sort(key=lambda _slot: _slot.start_dt)
    free_slots = []
    for i, slot in enumerate(slots):
        if slot.client_id is not None:
            # Слот занят
            continue

        if i == len(slots) - 1:
            free_slots.append(slot)
            break

        next_slot = slots[i + 1]
        dt = slot.start_dt + timedelta(minutes=execution_time_minutes)
        if dt <= next_slot.start_dt:
            free_slots.append(slot)

    return free_slots


class GetFreeTimetableSlotsExecutor(CommandExecutor):
    _service_provider: ServiceProvider
    _timetable_provider: TimetableProvider

    def __init__(self, db: DB):
        self._service_provider = ServiceProvider(db)
        self._timetable_provider = TimetableProvider(db)

    async def execute(self, command: GetFreeTimetableSlotsCommand) -> CommandResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды получения свободных слотов в расписании. {command}')

        execution_time_minutes = _get_services_execution_time(self._service_provider.get_by_ids(command.services))
        slots = self._timetable_provider.get_for_day(command.day, command.worker)
        slots = _filter_slots_by_execution_time(slots, execution_time_minutes)

        LoggerWrap().get_logger().info(f'Выполненена команда получения свободных слотов в расписании. {command}')
        return GetFreeTimetableSlotsResponse(
            command_id=command.id,
            status=CommandStatus.SUCCESSFUL_EXECUTION,
            timetable_ids=[slot.id for slot in slots]
        )
