from datetime import datetime, date, time, timedelta

from scheduler_core import containers
from scheduler_core.command_executors.command_executor import CommandExecutor
from scheduler_core.command_responses.get_worker_timetable import GetWorkerTimetableResponse
from scheduler_core.commands.get_worker_timetable import GetWorkerTimetableCommand
from scheduler_core.database import exceptions
from scheduler_core.database.db import DB
from scheduler_core.database.provider.timetable import TimetableProvider
from scheduler_core.enums import CommandStatus, TimeType, TimeLimit
from wrappers import LoggerWrap


WEEK_DAYS = 6
MONTH_DAYS = 29
START_TIME = time()
END_TIME = time(23, 59, 59)


def _get_data_ranges(today: date, time_type: TimeType, time_limit: TimeLimit) -> containers.DateRanges:
    if time_limit == TimeLimit.DAY:
        return containers.DateRanges(
            start_dt=datetime.combine(today, START_TIME),
            end_dt=datetime.combine(today, END_TIME),
        )

    if time_type == TimeType.PAST:
        if time_limit == TimeLimit.WEEK:
            return containers.DateRanges(
                start_dt=datetime.combine(today - timedelta(days=WEEK_DAYS), START_TIME),
                end_dt=datetime.combine(today, END_TIME),
            )
        if time_limit == TimeLimit.MONTH:
            return containers.DateRanges(
                start_dt=datetime.combine(today - timedelta(days=MONTH_DAYS), START_TIME),
                end_dt=datetime.combine(today, END_TIME),
            )
    if time_type == TimeType.FUTURE:
        if time_limit == TimeLimit.WEEK:
            return containers.DateRanges(
                start_dt=datetime.combine(today, START_TIME),
                end_dt=datetime.combine(today + timedelta(days=WEEK_DAYS), END_TIME),
            )
        if time_limit == TimeLimit.MONTH:
            return containers.DateRanges(
                start_dt=datetime.combine(today, START_TIME),
                end_dt=datetime.combine(today + timedelta(days=MONTH_DAYS), END_TIME),
            )


class GetWorkerTimetableExecutor(CommandExecutor):
    _timetable_provider: TimetableProvider

    def __init__(self, db: DB):
        self._timetable_provider = TimetableProvider(db)

    async def execute(self, command: GetWorkerTimetableCommand) -> GetWorkerTimetableResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды получения записей работника. {command}')

        data_ranges = _get_data_ranges(datetime.today(), command.time_type, command.time_limit)
        try:
            entries = self._timetable_provider.get_by_worker_id(command.worker, data_ranges)
        except exceptions.TimetableEntryIsNotFound as e:
            LoggerWrap().get_logger().info(str(e))
            return GetWorkerTimetableResponse(command_id=command.id, status=CommandStatus.NO_TIMETABLE_ENTRIES_FOUND)

        entries.sort(key=lambda x: x.id)
        LoggerWrap().get_logger().info(f'Найдены записи работника в расписании. entries={entries}')
        return GetWorkerTimetableResponse(
            command_id=command.id,
            status=CommandStatus.SUCCESSFUL_EXECUTION,
            timetable_entries=entries
        )
