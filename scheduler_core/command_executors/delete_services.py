from scheduler_core.command_executors.command_executor import CommandExecutor
from scheduler_core.command_responses.delete_services import DeleteServicesResponse
from scheduler_core.commands.delete_services import DeleteServicesCommand
from scheduler_core.database.db import DB
from scheduler_core.database.provider.service import ServiceProvider
from scheduler_core.enums import CommandStatus
from wrappers import LoggerWrap


class DeleteServicesExecutor(CommandExecutor):
    _service_provider: ServiceProvider

    def __init__(self, db: DB):
        self._service_provider = ServiceProvider(db)

    async def execute(self, command: DeleteServicesCommand) -> DeleteServicesResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды удаления списка услуг. {command}')

        self._service_provider.delete(command.services)
        LoggerWrap().get_logger().info(f'Выполнена команда удаления списка услуг. {command}')
        return DeleteServicesResponse(command_id=command.id, status=CommandStatus.SUCCESSFUL_EXECUTION)
