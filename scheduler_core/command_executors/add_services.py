from command_executors.command_executor import CommandExecutor
from command_responses.add_services import AddServicesResponse
from command_responses.command_response import CommandResponse
from commands.add_services import AddServicesCommand
from database import exceptions
from database.db import DB
from database.provider.service import ServiceProvider
from enums import CommandStatus
from wrappers import LoggerWrap


class AddServicesExecutor(CommandExecutor):
    _service_provider: ServiceProvider

    def __init__(self, db: DB):
        self._service_provider = ServiceProvider(db)

    async def execute(self, command: AddServicesCommand) -> CommandResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды добавления списка услуг. {command}')

        try:
            self._service_provider.multi_add(command.services)
        except exceptions.EntryAlreadyExists as e:
            LoggerWrap().get_logger().info(str(e))
            return AddServicesResponse(command_id=command.id, status=CommandStatus.SERVICE_ALREADY_EXISTS)

        LoggerWrap().get_logger().info(f'Выполненена команда добавления списка услуг. {command}')
        return AddServicesResponse(command_id=command.id, status=CommandStatus.SUCCESSFUL_EXECUTION)
