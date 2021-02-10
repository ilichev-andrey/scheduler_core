from command_executors.command_executor import CommandExecutor
from command_responses.command_response import CommandResponse
from command_responses.get_workers import GetWorkersResponse
from commands.get_workers import GetWorkersCommand
from database.db import DB
from database.provider.user import UserProvider
from enums import CommandStatus
from wrappers import LoggerWrap


class GetWorkersExecutor(CommandExecutor):
    _user_provider: UserProvider

    def __init__(self, db: DB):
        self._user_provider = UserProvider(db)

    async def execute(self, command: GetWorkersCommand) -> CommandResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды получения работников. {command}')

        workers = self._user_provider.get_workers()

        LoggerWrap().get_logger().info(f'Выполненена команда получения работников. {command}')
        return GetWorkersResponse(
            command_id=command.id,
            status=CommandStatus.SUCCESSFUL_EXECUTION,
            workers=workers
        )
