from command_executors.command_executor import CommandExecutor
from command_responses.add_user import AddUserResponse
from command_responses.command_response import CommandResponse
from commands.add_user import AddUserCommand
from database import exceptions
from database.containers import make_user
from database.db import DB
from database.enums import UserType
from database.provider.user import UserProvider
from enums import CommandStatus
from wrappers import LoggerWrap


class AddUserExecutor(CommandExecutor):
    _user_provider: UserProvider

    def __init__(self, db: DB):
        self._user_provider = UserProvider(db)

    async def execute(self, command: AddUserCommand) -> CommandResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды добавления пользователя. {command}')

        # Все добаляемые пользовалели по умолчанию являются клиентами
        user_data = command.user.asdict()
        user_data.pop('type', None)
        user = make_user(type=UserType.CLIENT, **user_data)

        try:
            self._user_provider.add(user)
        except exceptions.EntryAlreadyExists as e:
            LoggerWrap().get_logger().info(str(e))
            return AddUserResponse(command_id=command.id, status=CommandStatus.USER_ALREADY_EXISTS)

        LoggerWrap().get_logger().info(f'Выполненена команда добавления пользователя. {command}')
        return AddUserResponse(command_id=command.id, status=CommandStatus.SUCCESSFUL_EXECUTION)
