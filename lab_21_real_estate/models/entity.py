"""
Модуль базового абстрактного класса для всех сущностей системы.
"""
from abc import ABC, abstractmethod
from typing import Optional, Any
from datetime import datetime

from database.errors import ValidationError


class Entity(ABC):
    """
    Абстрактный базовый класс для всех сущностей системы.
    Реализует инкапсуляцию через приватные атрибуты и свойства.
    """
    
    def __init__(self, id: Optional[int] = None, title: str = "") -> None:
        self.__id = id
        self.__title = title
        self.__created_at: Optional[datetime] = None
        self.__updated_at: Optional[datetime] = None
    
    @property
    def id(self) -> Optional[int]:
        """Геттер для id."""
        return self.__id
    
    @id.setter
    def id(self, value: int) -> None:
        """Сеттер для id."""
        if value is not None and value < 0:
            raise ValidationError("ID не может быть отрицательным", "id")
        self.__id = value
    
    @property
    def title(self) -> str:
        """Геттер для title."""
        return self.__title
    
    @title.setter
    def title(self, value: str) -> None:
        """Сеттер для title."""
        if not isinstance(value, str):
            raise ValidationError("Title должен быть строкой", "title")
        self.__title = value
    
    @property
    def created_at(self) -> Optional[datetime]:
        """Геттер для created_at."""
        return self.__created_at
    
    @created_at.setter
    def created_at(self, value: datetime) -> None:
        """Сеттер для created_at."""
        self.__created_at = value
    
    @property
    def updated_at(self) -> Optional[datetime]:
        """Геттер для updated_at."""
        return self.__updated_at
    
    @updated_at.setter
    def updated_at(self, value: datetime) -> None:
        """Сеттер для updated_at."""
        self.__updated_at = value
    
    @abstractmethod
    def get_info(self) -> str:
        """
        Абстрактный метод для получения информации об объекте.
        Должен быть реализован в классах-наследниках.
        """
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """
        Абстрактный метод для валидации данных объекта.
        Должен быть реализован в классах-наследниках.
        """
        pass
    
    def to_dict(self) -> dict[str, Any]:
        """Преобразование объекта в словарь."""
        return {
            'id': self.__id,
            'title': self.__title,
            'created_at': self.__created_at.isoformat() if self.__created_at else None,
            'updated_at': self.__updated_at.isoformat() if self.__updated_at else None
        }
