from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, id=None, title=""):
        self._id = id
        self._title = title

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def validate(self) -> bool:
        pass