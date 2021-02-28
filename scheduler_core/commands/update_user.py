from typing import Dict

from scheduler_core.commands.command_with_user import CommandWithUser
from scheduler_core.enums import CommandType


class UpdateUserCommand(CommandWithUser):
    def __str__(self):
        return f'UpdateUserCommand(id={self.id}, user={self.user})'

    def get_type(self) -> CommandType:
        return CommandType.UPDATE_USER

    def _user_to_dict(self) -> Dict:
        user = self.user.asdict()
        user.pop('type')
        return user
