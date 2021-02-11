from typing import Dict, List

from commands.command import Command
from database.containers import Service, make_service
from enums import CommandType


class AddServicesCommand(Command):
    services: List[Service]

    def __init__(self, command_id: str = None, services: List[Service] = None):
        super().__init__(command_id=command_id)
        if services is None:
            services = []

        self.services = services

    def get_type(self) -> CommandType:
        return CommandType.ADD_SERVICES

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('services',)):
            return False

        if not isinstance(data['services'], List):
            return False

        if not super().load_from_dict(data):
            return False

        self.services = [make_service(id=None, **service) for service in data['services']]
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'services': [self._service_to_dict(service) for service in self.services]
        })
        return data

    @staticmethod
    def _service_to_dict(service: Service) -> Dict:
        data = service.asdict()
        data.pop('id')
        return data
