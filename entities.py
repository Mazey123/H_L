from abc import ABC, abstractmethod
from typing import Optional
import re

class Entity(ABC):
    """Абстрактный базовый класс для всех сущностей."""

    def __init__(self, id: Optional[int] = None, title: str = ""):
        self.__id = id
        self.__title = title

    @property
    def id(self) -> Optional[int]:
        return self.__id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        self.__id = value

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        self.__title = value

    @abstractmethod
    def get_info(self) -> str:
        """Возвращает строку с полной информацией об объекте."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Проверяет корректность данных объекта. Возвращает True, если данные валидны."""
        pass


class Apartment(Entity):
    """Класс, представляющий квартиру."""

    def __init__(self, id: Optional[int] = None, title: str = "",
                 address: str = "", area: float = 0.0,
                 rooms: int = 0, price: float = 0.0):
        super().__init__(id, title)
        self.__address = address
        self.__area = area
        self.__rooms = rooms
        self.__price = price

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str) -> None:
        self.__address = value

    @property
    def area(self) -> float:
        return self.__area

    @area.setter
    def area(self, value: float) -> None:
        self.__area = value

    @property
    def rooms(self) -> int:
        return self.__rooms

    @rooms.setter
    def rooms(self, value: int) -> None:
        self.__rooms = value

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        self.__price = value

    def get_info(self) -> str:
        return (f"Квартира [ID: {self.id}]: {self.title}\n"
                f"  Адрес: {self.address}\n"
                f"  Площадь: {self.area} кв.м, комнат: {self.rooms}\n"
                f"  Цена: {self.price} руб.")

    def validate(self) -> bool:
        if self.area <= 0:
            return False
        if self.rooms <= 0:
            return False
        if self.price <= 0:
            return False
        return True

    def price_per_sqm(self) -> float:
        """Дополнительный метод бизнес-логики: цена за квадратный метр."""
        if self.area > 0:
            return self.price / self.area
        return 0.0


class Client(Entity):
    """Класс, представляющий клиента."""

    def __init__(self, id: Optional[int] = None, title: str = "",
                 phone: str = "", email: str = ""):
        super().__init__(id, title)
        self.__phone = phone
        self.__email = email

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str) -> None:
        self.__phone = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        self.__email = value

    def get_info(self) -> str:
        return (f"Клиент [ID: {self.id}]: {self.title}\n"
                f"  Телефон: {self.phone}\n"
                f"  Email: {self.email}")

    def validate(self) -> bool:
        # Простейшая проверка телефона (наличие цифр) и email (наличие @)
        if not re.match(r"^\+?[0-9\s\-\(\)]{10,}$", self.phone):
            return False
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", self.email):
            return False
        return True


class Deal(Entity):
    """Класс, представляющий сделку с недвижимостью."""

    DEAL_TYPES = ("sale", "rent")

    def __init__(self, id: Optional[int] = None, title: str = "",
                 apartment_id: Optional[int] = None,
                 client_id: Optional[int] = None,
                 deal_type: str = "sale",
                 date: str = "",
                 amount: float = 0.0):
        super().__init__(id, title)
        self.__apartment_id = apartment_id
        self.__client_id = client_id
        self.__deal_type = deal_type
        self.__date = date
        self.__amount = amount

    @property
    def apartment_id(self) -> Optional[int]:
        return self.__apartment_id

    @apartment_id.setter
    def apartment_id(self, value: Optional[int]) -> None:
        self.__apartment_id = value

    @property
    def client_id(self) -> Optional[int]:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: Optional[int]) -> None:
        self.__client_id = value

    @property
    def deal_type(self) -> str:
        return self.__deal_type

    @deal_type.setter
    def deal_type(self, value: str) -> None:
        if value in self.DEAL_TYPES:
            self.__deal_type = value
        else:
            raise ValueError(f"Тип сделки должен быть одним из {self.DEAL_TYPES}")

    @property
    def date(self) -> str:
        return self.__date

    @date.setter
    def date(self, value: str) -> None:
        self.__date = value

    @property
    def amount(self) -> float:
        return self.__amount

    @amount.setter
    def amount(self, value: float) -> None:
        self.__amount = value

    def get_info(self) -> str:
        return (f"Сделка [ID: {self.id}]: {self.title}\n"
                f"  Квартира ID: {self.apartment_id}\n"
                f"  Клиент ID: {self.client_id}\n"
                f"  Тип: {self.deal_type}, Дата: {self.date}\n"
                f"  Сумма: {self.amount} руб.")

    def validate(self) -> bool:
        if self.apartment_id is None or self.apartment_id <= 0:
            return False
        if self.client_id is None or self.client_id <= 0:
            return False
        if self.deal_type not in self.DEAL_TYPES:
            return False
        if not self.date:
            return False
        if self.amount <= 0:
            return False
        return True

    def commission(self, rate: float = 0.03) -> float:
        """Дополнительный метод: расчёт комиссии агента."""
        return self.amount * rate