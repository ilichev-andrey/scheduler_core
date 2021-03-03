from scheduler_core.command_executors.command_executor import CommandExecutor
from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.command_responses.get_services import GetServicesResponse
from scheduler_core.commands.get_services import GetServicesCommand
from scheduler_core.database import exceptions
from scheduler_core.database.db import DB
from scheduler_core.database.provider.service import ServiceProvider
from scheduler_core.enums import CommandStatus
from wrappers import LoggerWrap


class GetServicesExecutor(CommandExecutor):
    _service_provider: ServiceProvider

    def __init__(self, db: DB):
        self._service_provider = ServiceProvider(db)

    async def execute(self, command: GetServicesCommand) -> CommandResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды получения списка услуг. {command}')

        try:
            services = self._service_provider.get()
        except exceptions.ServiceIsNotFound as e:
            LoggerWrap().get_logger().info(str(e))
            return GetServicesResponse(command_id=command.id, status=CommandStatus.NO_SERVICES_FOUND)

        LoggerWrap().get_logger().info(f'Выполнена команда получения списка услуг. {command}')
        return GetServicesResponse(command_id=command.id, status=CommandStatus.SUCCESSFUL_EXECUTION, services=services)
