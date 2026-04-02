"""
Модуль модели клиента для системы управления недвижимостью.
"""
from typing import Optional, Any

from database.errors import ValidationError
from models.entity import Entity


class Client(Entity):
    """
    Класс клиента - наследник абстрактного класса Entity.
    Представляет покупателя или арендатора недвижимости.
    """
    
    TABLE_NAME = 'clients'
    
    def __init__(
        self,
        id: Optional[int] = None,
        full_name: str = "",
        phone: str = "",
        email: str = "",
        passport_series: str = "",
        passport_number: str = ""
    ) -> None:
        super().__init__(id, full_name)
        self.__full_name = full_name
        self.__phone = phone
        self.__email = email
        self.__passport_series = passport_series
        self.__passport_number = passport_number
        self.__bonus_points: int = 0
        self.__deal_count: int = 0
    
    # Геттеры и сеттеры
    @property
    def full_name(self) -> str:
        return self.__full_name
    
    @full_name.setter
    def full_name(self, value: str) -> None:
        if not value or len(value) > 200:
            raise ValidationError("ФИО должно быть от 1 до 200 символов", "full_name")
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
    def passport_series(self) -> str:
        return self.__passport_series
    
    @passport_series.setter
    def passport_series(self, value: str) -> None:
        self.__passport_series = value[:10] if value else ""
    
    @property
    def passport_number(self) -> str:
        return self.__passport_number
    
    @passport_number.setter
    def passport_number(self, value: str) -> None:
        self.__passport_number = value[:20] if value else ""
    
    @property
    def bonus_points(self) -> int:
        return self.__bonus_points
    
    @property
    def deal_count(self) -> int:
        return self.__deal_count
    
    # Бизнес-методы
    def add_bonus(self, points: int) -> None:
        """Начисление бонусных баллов клиенту."""
        if points < 0:
            raise ValidationError("Бонусные баллы не могут быть отрицательными", "bonus_points")
        self.__bonus_points += points
    
    def use_bonus(self, points: int) -> bool:
        """Использование бонусных баллов."""
        if points <= 0 or points > self.__bonus_points:
            return False
        self.__bonus_points -= points
        return True
    
    def increment_deal_count(self) -> None:
        """Увеличение счетчика сделок."""
        self.__deal_count += 1
    
    def get_client_status(self) -> str:
        """Получение статуса клиента на основе количества сделок."""
        if self.__deal_count == 0:
            return "Новый"
        elif self.__deal_count <= 2:
            return "Постоянный"
        elif self.__deal_count <= 5:
            return "VIP"
        else:
            return "Премиум"
    
    def get_discount_rate(self) -> float:
        """Получение процентной ставки скидки для клиента."""
        rates = {
            "Новый": 0.0,
            "Постоянный": 0.5,
            "VIP": 1.0,
            "Премиум": 2.0
        }
        return rates.get(self.get_client_status(), 0.0)
    
    # Реализация абстрактных методов
    def get_info(self) -> str:
        """Формирование полной информации о клиенте."""
        return (
            f"Клиент: {self.__full_name}\n"
            f"Телефон: {self.__phone}\n"
            f"Email: {self.__email or 'Не указан'}\n"
            f"Паспорт: {self.__passport_series} {self.__passport_number or 'Не указан'}\n"
            f"Статус: {self.get_client_status()}\n"
            f"Бонусные баллы: {self.__bonus_points}\n"
            f"Количество сделок: {self.__deal_count}\n"
            f"Скидка: {self.get_discount_rate()}%"
        )
    
    def validate(self) -> bool:
        """Валидация данных клиента."""
        try:
            if not self.__full_name:
                raise ValidationError("ФИО обязательно", "full_name")
            if not self.__phone:
                raise ValidationError("Телефон обязателен", "phone")
            if self.__email and '@' not in self.__email:
                raise ValidationError("Некорректный email", "email")
            return True
        except ValidationError:
            return False
    
    def to_dict(self) -> dict[str, Any]:
        """Преобразование объекта в словарь."""
        data = super().to_dict()
        data.update({
            'full_name': self.__full_name,
            'phone': self.__phone,
            'email': self.__email,
            'passport_series': self.__passport_series,
            'passport_number': self.__passport_number,
            'bonus_points': self.__bonus_points,
            'deal_count': self.__deal_count
        })
        return data
