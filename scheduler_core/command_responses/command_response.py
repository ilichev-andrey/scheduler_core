from abc import abstractmethod
from typing import Dict, Set

from scheduler_core.enums import CommandStatus, CommandType
from scheduler_core.interfaces import Serializable


class CommandResponse(Serializable):
    id = str
    status: CommandStatus

    def __init__(self, command_id: str = None, status: CommandStatus = None):
        if command_id is None:
            command_id = ''

        if status is None:
            status = CommandStatus.UNKNOWN

        self.id = command_id
        self.status = status

    @abstractmethod
    def get_command_type(self) -> CommandType:
        pass

    @abstractmethod
    def _load_data(self, data: Dict) -> bool:
        pass

    @abstractmethod
    def _unload_data(self) -> Dict:
        pass

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('id', 'status')):
            return False

        if not super()._has_keys_in_dict(data['status'], ('code',)):
            return False

        status = CommandStatus(data['status']['code'])
        if not self._load_data_if_successful_status(data, status):
            return False

        self.id = str(data['id'])
        self.status = status
        return True

    def to_dict(self) -> Dict:
        data = {
            'id': self.id,
            'type': self.get_command_type().value,
            'status': {
                'code': self.status.value,
                'message': self.status.name
            }
        }
        data.update(self._unload_data_if_successful_status())
        return data

    @staticmethod
    def _get_successful_statuses() -> Set[CommandStatus]:
        return {CommandStatus.SUCCESSFUL_EXECUTION}

    def _load_data_if_successful_status(self, data: Dict, status: CommandStatus) -> bool:
        # Загрузка дополнительных данных только при статусах успешного выполнения
        if status in self._get_successful_statuses():
            return self._load_data(data)

        return True

    def _unload_data_if_successful_status(self) -> Dict:
        # Выгрузка дополнительных данных только при статусах успешного выполнения
        if self.status in self._get_successful_statuses():
            return self._unload_data()

        return {}
