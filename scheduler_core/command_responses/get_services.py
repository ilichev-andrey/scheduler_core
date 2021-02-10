from typing import Dict, List

from command_responses.command_response import CommandResponse
from database.containers import Service, make_service
from enums import CommandStatus, CommandType


class GetServicesResponse(CommandResponse):
    services: List[Service]

    def __init__(self, command_id: str = None, status: CommandStatus = None, services: List[Service] = None):
        super().__init__(command_id=command_id, status=status)
        if services is None:
            services = []

        self.services = services

    def get_command_type(self) -> CommandType:
        return CommandType.GET_SERVICES

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('services',)):
            return False

        if not isinstance(data['services'], List):
            return False

        if not super().load_from_dict(data):
            return False

        self.services = [make_service(**service_data) for service_data in data['services']]
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'services': [service.asdict() for service in self.services]
        })
        return data
