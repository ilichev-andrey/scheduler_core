from scheduler_core.command_executors.command_executor import CommandExecutor
from scheduler_core.command_responses.get_client_timetable import GetClientTimetableResponse
from scheduler_core.commands.get_client_timetable import GetClientTimetableCommand
from scheduler_core.database import exceptions
from scheduler_core.database.db import DB
from scheduler_core.database.provider.timetable import TimetableProvider
from scheduler_core.enums import CommandStatus
from wrappers import LoggerWrap


class GetClientTimetableExecutor(CommandExecutor):
    _timetable_provider: TimetableProvider

    def __init__(self, db: DB):
        self._timetable_provider = TimetableProvider(db)

    async def execute(self, command: GetClientTimetableCommand) -> GetClientTimetableResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды получения записей клиента. {command}')

        try:
            entries = self._timetable_provider.get_by_client_id(command.client, command.limit)
        except exceptions.TimetableEntryIsNotFound as e:
            LoggerWrap().get_logger().info(str(e))
            return GetClientTimetableResponse(command_id=command.id, status=CommandStatus.NO_TIMETABLE_ENTRIES_FOUND)

        LoggerWrap().get_logger().info(f'Найдены записи клиента в расписании. entries={entries}')
        return GetClientTimetableResponse(
            command_id=command.id,
            status=CommandStatus.SUCCESSFUL_EXECUTION,
            timetable_entries=entries
        )
