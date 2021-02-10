from typing import Dict, List

from command_responses.command_response import CommandResponse
from database.containers import User, make_user
from enums import CommandStatus, CommandType


class GetWorkersResponse(CommandResponse):
    workers: List[User]

    def __init__(self, command_id: str = None, status: CommandStatus = None, workers: List[User] = None):
        super().__init__(command_id=command_id, status=status)
        if workers is None:
            workers = []

        self.workers = workers

    def get_command_type(self) -> CommandType:
        return CommandType.GET_WORKERS

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('workers',)):
            return False

        if not isinstance(data['workers'], List):
            return False

        if not super().load_from_dict(data):
            return False

        self.workers = [make_user(**worker_data) for worker_data in data['workers']]
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'workers': [worker.asdict() for worker in self.workers]
        })
        return data
