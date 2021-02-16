from typing import Dict

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.database.containers import User, make_user
from scheduler_core.enums import CommandType, CommandStatus


class GetUserResponse(CommandResponse):
    user: User

    def __init__(self, command_id: str = None, status: CommandStatus = None, user: User = None):
        super().__init__(command_id=command_id, status=status)
        if user is None:
            user = User()

        self.user = user

    def get_command_type(self) -> CommandType:
        return CommandType.GET_USER

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
        data.update({'user': self.user.asdict()})
        return data
