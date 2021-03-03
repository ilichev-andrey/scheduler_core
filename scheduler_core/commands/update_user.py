from typing import Dict

from scheduler_core.commands.command_with_user import CommandWithUser
from scheduler_core.containers import User, make_user
from scheduler_core.enums import CommandType


class UpdateUserCommand(CommandWithUser):
    def __str__(self):
        return f'UpdateUserCommand(id={self.id}, user={self.user})'

    def get_type(self) -> CommandType:
        return CommandType.UPDATE_USER

    def _user_from_dict(self, data: Dict) -> User:
        data = self._delete_service_params(data)
        return make_user(**data)

    def _user_to_dict(self) -> Dict:
        user = self.user.asdict()
        return self._delete_service_params(user)

    @staticmethod
    def _delete_service_params(data: Dict) -> Dict:
        data.pop('type', None)
        return data

