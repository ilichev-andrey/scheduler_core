from typing import Dict, List

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.database.containers import User, make_user
from scheduler_core.enums import CommandStatus, CommandType


class GetWorkersResponse(CommandResponse):
    workers: List[User]

    def __init__(self, command_id: str = None, status: CommandStatus = None, workers: List[User] = None):
        super().__init__(command_id=command_id, status=status)
        if workers is None:
            workers = []

        self.workers = workers

    def get_command_type(self) -> CommandType:
        return CommandType.GET_WORKERS

    def _load_data(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('workers',)):
            return False

        if not isinstance(data['workers'], List):
            return False

        self.workers = [make_user(**worker_data) for worker_data in data['workers']]
        return True

    def _unload_data(self) -> Dict:
        return {'workers': [worker.asdict() for worker in self.workers]}
