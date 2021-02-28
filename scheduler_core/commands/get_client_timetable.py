from typing import Dict

from scheduler_core.commands.command import Command
from scheduler_core.enums import CommandType


class GetClientTimetableCommand(Command):
    client: int
    limit: int

    def __init__(self, command_id: str = None, client: int = None, limit: int = None):
        super().__init__(command_id=command_id)
        if client is None:
            client = 0

        if limit is None:
            limit = 10

        self.client = client
        self.limit = limit

    def __str__(self):
        return f'GetClientTimetableSlotsCommand(id={self.id}, client={self.client}, limit={self.limit})'

    def get_type(self) -> CommandType:
        return CommandType.GET_CLIENT_TIMETABLE

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('client', 'limit')):
            return False

        if not super().load_from_dict(data):
            return False

        self.client = data['client']
        self.limit = data['limit']
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'client': self.client,
            'limit': self.limit
        })
        return data
