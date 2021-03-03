from typing import Dict

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.containers import User, make_user
from scheduler_core.enums import CommandType, CommandStatus


class ResponseWithUser(CommandResponse):
    user: User

    def __init__(self, command_id: str = None, status: CommandStatus = None, user: User = None):
        super().__init__(command_id=command_id, status=status)
        if user is None:
            user = User()

        self.user = user

    def __str__(self):
        return f'ResponseWithUser(id={self.id}, status={self.status}, user={self.user})'

    def get_command_type(self) -> CommandType:
        return CommandType.UNKNOWN

    def _load_data(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('user',)):
            return False

        if not isinstance(data['user'], Dict):
            return False

        self.user = make_user(**data['user'])
        return True

    def _unload_data(self) -> Dict:
        return {'user': self.user.asdict()}
