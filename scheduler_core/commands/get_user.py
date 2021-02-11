from typing import Dict

from commands.command import Command
from enums import CommandType


class GetUserCommand(Command):
    telegram_id: int or None
    viber_id: int or None

    def __init__(self, command_id: str = None, telegram_id: int = None, viber_id: int = None):
        super().__init__(command_id=command_id)
        self.telegram_id = telegram_id
        self.viber_id = viber_id

    def get_type(self) -> CommandType:
        return CommandType.GET_USER

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('user', )):
            return False

        user_data = data['user']
        if not super()._has_keys_in_dict(user_data, ('telegram_id', 'viber_id')):
            return False

        if user_data['telegram_id'] is None and user_data['viber_id'] is None:
            return False

        if not super().load_from_dict(data):
            return False

        self.telegram_id = user_data['telegram_id']
        self.viber_id = user_data['viber_id']
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'user': {
                'telegram_id': self.telegram_id,
                'viber_id': self.viber_id
            }
        })
        return data
