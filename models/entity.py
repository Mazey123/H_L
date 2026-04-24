from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, id: int | None = None, title: str = "") -> None:
        self.__id = id
        self.__title = title

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        if value is not None and value < 0:
            raise ValueError("ID не может быть отрицательным")
        self.__id = value

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        self.__title = value

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def validate(self) -> bool:
        pass