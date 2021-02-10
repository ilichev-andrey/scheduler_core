from command_executors.command_executor import CommandExecutor
from command_responses.command_response import CommandResponse
from command_responses.get_services import GetServicesResponse
from commands.get_services import GetServicesCommand
from database.db import DB
from database.provider.service import ServiceProvider
from enums import CommandStatus
from wrappers import LoggerWrap


class GetServicesExecutor(CommandExecutor):
    _service_provider: ServiceProvider

    def __init__(self, db: DB):
        self._service_provider = ServiceProvider(db)

    async def execute(self, command: GetServicesCommand) -> CommandResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды получения списка услуг. {command}')

        services = self._service_provider.get()

        LoggerWrap().get_logger().info(f'Выполненена команда получения списка услуг. {command}')
        return GetServicesResponse(command_id=command.id, status=CommandStatus.SUCCESSFUL_EXECUTION, services=services)
