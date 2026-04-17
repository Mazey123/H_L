from typing import Optional, Any

from database.errors import ValidationError
from models.entity import Entity


class Client(Entity):
    """
    Представляет покупателя недвижимости.
    """
    
    TABLE_NAME = 'clients'
    
    def __init__(
        self,
        id: Optional[int] = None,
        full_name: str = "",
        phone: str = "",
        email: str = ""
    ) -> None:
        super().__init__(id, full_name)
        self.__full_name = full_name
        self.__phone = phone
        self.__email = email
        self.__deal_count: int = 0

    
    # Геттеры и сеттеры
    @property
    def full_name(self) -> str:
        return self.__full_name
    
    @full_name.setter
    def full_name(self, value: str) -> None:
        if not value or len(value) > 100:
            raise ValidationError("ФИО должно быть от 1 до 100 символов", "full_name")
        self.__full_name = value
    
    @property
    def phone(self) -> str:
        return self.__phone
    
    @phone.setter
    def phone(self, value: str) -> None:
        if not value or len(value) > 20:
            raise ValidationError("Некорректный номер телефона", "phone")
        self.__phone = value
    
    @property
    def email(self) -> str:
        return self.__email
    
    @email.setter
    def email(self, value: str) -> None:
        if value and '@' not in value:
            raise ValidationError("Некорректный email", "email")
        self.__email = value[:100] if value else ""

    @property
    def deal_count(self) -> int:
        return self.__deal_count
    
    def add_deal_count(self) -> None:
        """Увеличение счетчика сделок."""
        self.__deal_count += 1
    
    def get_client_status(self) -> str:
        """Получение статуса клиента на основе количества сделок."""
        if self.__deal_count == 0:
            return "Новый"
        elif self.__deal_count <= 2:
            return "Постоянный"
        elif self.__deal_count <= 5:
            return "Лега"
        else:
            return "Откуда деньги?"

    # Реализация абстрактных методов
    def get_info(self) -> str:
        """Формирование полной информации о клиенте."""
        return (
            f"Клиент: {self.__full_name}\n"
            f"Телефон: {self.__phone}\n"
            f"Email: {self.__email or 'Не указан'}\n"
            f"Статус: {self.get_client_status()}\n"
        )
    
    def validate(self) -> bool:
        """Валидация данных клиента."""
        if not self.__full_name:
            raise ValidationError("ФИО обязательно", "full_name")
        if not self.__phone:
            raise ValidationError("Телефон обязателен", "phone")
        if self.__email and '@' not in self.__email:
            raise ValidationError("Некорректный email", "email")
        return True

    def to_dict(self) -> dict[str, Any]:
        """Преобразование объекта в словарь."""
        data = super().to_dict()
        data.update({
            'full_name': self.__full_name,
            'phone': self.__phone,
            'email': self.__email,
        })
        return data
