from scheduler_core.command_executors.command_executor import CommandExecutor
from scheduler_core.command_responses.update_user import UpdateUserResponse
from scheduler_core.commands.update_user import UpdateUserCommand
from scheduler_core.containers import User
from scheduler_core.database.db import DB
from scheduler_core.database.provider.user import UserProvider
from scheduler_core.enums import CommandStatus
from wrappers import LoggerWrap


class UpdateUserExecutor(CommandExecutor):
    _user_provider: UserProvider

    def __init__(self, db: DB):
        self._user_provider = UserProvider(db)

    async def execute(self, command: UpdateUserCommand) -> UpdateUserResponse:
        LoggerWrap().get_logger().info(f'Выполнение команды обновления информации пользователя. {command}')

        user = command.user
        _user = User(id=user.id, first_name=user.first_name, last_name=user.last_name, phone_number=user.phone_number,
                     telegram_name=user.telegram_name, viber_name=user.viber_name)

        self._user_provider.update(_user)

        LoggerWrap().get_logger().info(f'Выполнена команда обновления информации пользователя. {command}')
        return UpdateUserResponse(command_id=command.id, status=CommandStatus.SUCCESSFUL_EXECUTION)
