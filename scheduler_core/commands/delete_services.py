from typing import FrozenSet, Dict, List

from scheduler_core.commands.command import Command
from scheduler_core.enums import CommandType


class DeleteServicesCommand(Command):
    services: FrozenSet[int]

    def __init__(self, command_id: str = None, services: FrozenSet[int] = None):
        super().__init__(command_id=command_id)

        if services is None:
            services = frozenset()

        self.services = services

    def __str__(self):
        return f'DeleteServicesCommand(id={self.id}, services={self.services})'

    def get_type(self) -> CommandType:
        return CommandType.DELETE_SERVICES

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('services',)):
            return False

        if not isinstance(data['services'], List):
            return False

        if not super().load_from_dict(data):
            return False

        self.services = frozenset(data['services'])
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'services': list(self.services)
        })
        return data
