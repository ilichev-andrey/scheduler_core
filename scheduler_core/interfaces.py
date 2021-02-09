from abc import ABC, ABCMeta, abstractmethod
from typing import Dict, Iterable


class LoadableFromDict(ABC):
    @abstractmethod
    def load_from_dict(self, data: Dict) -> bool:
        pass

    @staticmethod
    def _has_keys_in_dict(data: Dict, keys: Iterable) -> bool:
        for key in keys:
            if key not in data:
                return False
        return True


class ConvertibleToDict(ABC):
    @abstractmethod
    def to_dict(self) -> Dict:
        pass


class Serializable(LoadableFromDict, ConvertibleToDict, metaclass=ABCMeta):
    pass
