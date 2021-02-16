from scheduler_core.command_executors.command_executor import CommandExecutor
from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.command_responses.get_workers import GetWorkersResponse
from scheduler_core.commands.get_workers import GetWorkersCommand
from scheduler_core.database.db import DB
from scheduler_core.database.provider.user import UserProvider
from scheduler_core.enums import CommandStatus
from wrappers import LoggerWrap


class GetWorkersExecutor(CommandExecutor):
    _user_provider: UserProvider

    def __init__(self, db: DB):
        self._user_provider = UserProvider(db)

    async def execute(self, command: GetWorkersCommand) -> CommandResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды получения работников. {command}')

        workers = self._user_provider.get_workers()

        LoggerWrap().get_logger().info(f'Выполнена команда получения работников. {command}')
        return GetWorkersResponse(
            command_id=command.id,
            status=CommandStatus.SUCCESSFUL_EXECUTION,
            workers=workers
        )
