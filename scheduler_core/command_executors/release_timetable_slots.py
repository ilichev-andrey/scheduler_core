from scheduler_core.command_executors.command_executor import CommandExecutor
from scheduler_core.command_responses.release_timetable_slot import ReleaseTimetableSlotsResponse
from scheduler_core.commands.release_timetable_slot import ReleaseTimetableSlotsCommand
from scheduler_core.database.db import DB
from scheduler_core.database.provider.timetable import TimetableProvider
from scheduler_core.enums import CommandStatus
from wrappers import LoggerWrap


class ReleaseTimetableSlotsExecutor(CommandExecutor):
    _timetable_provider: TimetableProvider

    def __init__(self, db: DB):
        self._timetable_provider = TimetableProvider(db)

    async def execute(self, command: ReleaseTimetableSlotsCommand) -> ReleaseTimetableSlotsResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды освобождения слотов расписания. {command}')

        entries = self._timetable_provider.release_entries(command.timetable_entries)
        entries.sort(key=lambda entry: entry.id)
        return ReleaseTimetableSlotsResponse(
            command_id=command.id,
            status=CommandStatus.SUCCESSFUL_EXECUTION,
            timetable_entries=entries
        )
