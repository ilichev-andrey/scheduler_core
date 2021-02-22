from scheduler_core.command_executors.command_executor import CommandExecutor
from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.command_responses.get_user import GetUserResponse
from scheduler_core.commands.get_user import GetUserCommand
from scheduler_core.database import exceptions
from scheduler_core.database.db import DB
from scheduler_core.database.provider.user import UserProvider
from scheduler_core.enums import CommandStatus
from wrappers import LoggerWrap


class GetUserExecutor(CommandExecutor):
    _user_provider: UserProvider

    def __init__(self, db: DB):
        self._user_provider = UserProvider(db)

    async def execute(self, command: GetUserCommand) -> CommandResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды получения пользователя. {command}')

        try:
            user = self._user_provider.get_buy_messenger_id(telegram_id=command.telegram_id, viber_id=command.viber_id)
        except exceptions.UserIsNotFound as e:
            LoggerWrap().get_logger().info(str(e))
            return GetUserResponse(command_id=command.id, status=CommandStatus.USER_IS_NOT_FOUND)

        LoggerWrap().get_logger().info(f'Выполнена команда получения пользователя. {command}')
        return GetUserResponse(command_id=command.id, status=CommandStatus.SUCCESSFUL_EXECUTION, user=user)
