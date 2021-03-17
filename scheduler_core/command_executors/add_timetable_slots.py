from datetime import datetime, timedelta, date, time
from typing import FrozenSet, List

from scheduler_core import containers

from scheduler_core.command_executors.command_executor import CommandExecutor
from scheduler_core.command_responses.add_timetable_slots import AddTimetableSlotsResponse
from scheduler_core.commands.add_timetable_slots import AddTimetableSlotsCommand
from scheduler_core.database import exceptions
from scheduler_core.database.db import DB
from scheduler_core.database.provider.timetable import TimetableProvider
from scheduler_core.enums import CommandStatus
from wrappers import LoggerWrap


def generate_start_dts(date_ranges: containers.DateRanges, times: List[time],
                       exclude_days: FrozenSet[date]) -> List[datetime]:
    start = date_ranges.start_dt
    end = date_ranges.end_dt
    dates = []
    for i in range(0, (end - start).days + 1):
        _date = (start + timedelta(days=i)).date()
        if _date in exclude_days:
            continue

        for _time in times:
            dates.append(datetime.combine(_date, _time))

    return dates


class AddTimetableSlotsExecutor(CommandExecutor):
    _timetable_provider: TimetableProvider

    def __init__(self, db: DB):
        self._timetable_provider = TimetableProvider(db)

    async def execute(self, command: AddTimetableSlotsCommand) -> AddTimetableSlotsResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды добавления слотов в расписание. {command}')

        try:
            entries = self._timetable_provider.get_by_worker_id(command.worker, command.date_ranges)
        except exceptions.TimetableEntryIsNotFound:
            entries = []

        start_dts = generate_start_dts(
            date_ranges=command.date_ranges,
            times=command.times,
            exclude_days=frozenset(entry.start_dt.date() for entry in entries)
        )

        if start_dts:
            self._timetable_provider.add(command.worker, start_dts)
        return AddTimetableSlotsResponse(
            command_id=command.id,
            status=CommandStatus.SUCCESSFUL_EXECUTION,
            dates=start_dts
        )
