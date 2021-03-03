from typing import Dict

from scheduler_core.commands.command import Command
from scheduler_core.enums import CommandType, TimeLimit, TimeType


class GetWorkerTimetableCommand(Command):
    worker: int
    time_type: TimeType
    time_limit: TimeLimit

    def __init__(self, command_id: str = None, worker: int = None, time_type: TimeType = None,
                 time_limit: TimeLimit = None):
        super().__init__(command_id=command_id)
        if worker is None:
            worker = 0

        if time_type is None:
            time_type = TimeType.UNKNOWN

        if time_limit is None:
            time_limit = TimeLimit.UNKNOWN

        self.worker = worker
        self.time_type = time_type
        self.time_limit = time_limit

    def __str__(self):
        return f'GetWorkerTimetableCommand(id={self.id}, worker={self.worker}, time_type={self.time_type}, ' \
               f'time_limit={self.time_limit})'

    def get_type(self) -> CommandType:
        return CommandType.GET_WORKER_TIMETABLE

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('worker', 'time_type', 'time_limit')):
            return False

        if not super().load_from_dict(data):
            return False

        self.worker = data['worker']
        self.time_type = TimeType(data['time_type'])
        self.time_limit = TimeLimit(data['time_limit'])
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'worker': self.worker,
            'time_type': self.time_type.value,
            'time_limit': self.time_limit.value
        })
        return data
