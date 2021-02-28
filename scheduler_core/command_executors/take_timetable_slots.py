from scheduler_core.command_executors.command_executor import CommandExecutor
from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.command_responses.take_timetable_slots import TakeTimetableSlotsResponse
from scheduler_core.commands.take_timetable_slots import TakeTimetableSlotsCommand
from scheduler_core.database import exceptions
from scheduler_core.database.db import DB
from scheduler_core.database.provider.service import ServiceProvider
from scheduler_core.database.provider.timetable import TimetableProvider
from scheduler_core.enums import CommandStatus
from wrappers import LoggerWrap


class TakeTimetableSlotsExecutor(CommandExecutor):
    _service_provider: ServiceProvider
    _timetable_provider: TimetableProvider

    def __init__(self, db: DB):
        self._service_provider = ServiceProvider(db)
        self._timetable_provider = TimetableProvider(db)

    async def execute(self, command: TakeTimetableSlotsCommand) -> CommandResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды записи клиента. {command}')

        services = self._service_provider.get_by_ids(command.services)
        try:
            self._timetable_provider.sign_up_client(command.timetable_entries, services, command.client)
        except exceptions.EntryAlreadyExists as e:
            LoggerWrap().get_logger().info(str(e))
            LoggerWrap().get_logger().info('Не удалось записать клиента')
            return TakeTimetableSlotsResponse(command_id=command.id, status=CommandStatus.SLOT_ALREADY_BUSY)

        LoggerWrap().get_logger().info(f'Успешное выполнение записи клиента')
        return TakeTimetableSlotsResponse(command_id=command.id, status=CommandStatus.SUCCESSFUL_EXECUTION)
