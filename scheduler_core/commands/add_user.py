from scheduler_core.commands.command_with_user import CommandWithUser
from scheduler_core.enums import CommandType


class AddUserCommand(CommandWithUser):
    def __str__(self):
        return f'AddUserCommand(id={self.id}, user={self.user})'

    def get_type(self) -> CommandType:
        return CommandType.ADD_USER
