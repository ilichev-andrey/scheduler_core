from typing import Dict

from commands.command import Command
from database.containers import User, make_user
from enums import CommandType


class AddUserCommand(Command):
    user: User

    def __init__(self, command_id: str = None, user: User = None):
        super().__init__(command_id=command_id)
        if user is None:
            user = User()

        self.user = user

    def get_type(self) -> CommandType:
        return CommandType.ADD_USER

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('user',)):
            return False

        if not isinstance(data['user'], Dict):
            return False

        if not super().load_from_dict(data):
            return False

        self.user = make_user(**data['user'])
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({'user': self._user_to_dict()})
        return data

    def _user_to_dict(self) -> Dict:
        user = self.user.asdict()
        user.pop('id')
        user.pop('type')
        return user
