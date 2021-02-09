from typing import Dict

from enums import CommandStatus
from interfaces import Serializable


class CommandResponse(Serializable):
    id = str
    status: CommandStatus

    def __init__(self, command_id='', status=CommandStatus.UNKNOWN):
        self.id = command_id
        self.status = status

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('id', 'status')):
            return False

        if not super()._has_keys_in_dict(data['status'], ('code',)):
            return False

        self.id = str(data['id'])
        self.status = CommandStatus(data['status']['code'])
        return True

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'status': {
                'code': self.status.value,
                'message': self.status.name
            }
        }
