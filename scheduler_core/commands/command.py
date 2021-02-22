import random
import string
from abc import abstractmethod
from typing import Dict

from scheduler_core.enums import CommandType
from scheduler_core.interfaces import Serializable


class Command(Serializable):
    ID_LENGTH = 10
    id = str

    def __init__(self, command_id: str = None):
        if command_id is None:
            command_id = self._generate_command_id()

        self.id = command_id

    def __str__(self):
        return f'Command(id={self.id})'

    @abstractmethod
    def get_type(self) -> CommandType:
        pass

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('id',)):
            return False

        self.id = str(data['id'])
        return True

    def to_dict(self) -> Dict:
        return {'id': self.id, 'type': self.get_type().value}

    def _generate_command_id(self) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=self.ID_LENGTH))
