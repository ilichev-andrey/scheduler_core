from command_executors.command_executor import CommandExecutor
from command_responses.command_response import CommandResponse
from command_responses.get_user import GetUserResponse
from commands.get_user import GetUserCommand
from database.db import DB
from database.provider.user import UserProvider
from enums import CommandStatus
from wrappers import LoggerWrap


class GetUserExecutor(CommandExecutor):
    _user_provider: UserProvider

    def __init__(self, db: DB):
        self._user_provider = UserProvider(db)

    async def execute(self, command: GetUserCommand) -> CommandResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды добавления получения пользователя. {command}')

        user = self._user_provider.get_buy_messenger_id(telegram_id=command.telegram_id, viber_id=command.viber_id)

        LoggerWrap().get_logger().info(f'Выполненена команда добавления получения пользователя. {command}')
        return GetUserResponse(command_id=command.id, status=CommandStatus.SUCCESSFUL_EXECUTION, user=user)
