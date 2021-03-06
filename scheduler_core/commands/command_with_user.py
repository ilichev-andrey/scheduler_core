from typing import Dict

from scheduler_core.commands.command import Command
from scheduler_core.containers import User, make_user
from scheduler_core.enums import CommandType


class CommandWithUser(Command):
    user: User

    def __init__(self, command_id: str = None, user: User = None):
        super().__init__(command_id=command_id)
        if user is None:
            user = User()

        self.user = user

    def __str__(self):
        return f'CommandWithUser(id={self.id}, user={self.user})'

    def get_type(self) -> CommandType:
        return CommandType.UNKNOWN

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('user',)):
            return False

        if not isinstance(data['user'], Dict):
            return False

        if not super().load_from_dict(data):
            return False

        self.user = self._user_from_dict(data['user'])
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({'user': self._user_to_dict()})
        return data

    @staticmethod
    def _user_from_dict(data: Dict) -> User:
        return make_user(**data)

    def _user_to_dict(self) -> Dict:
        user = self.user.asdict()
        return user
