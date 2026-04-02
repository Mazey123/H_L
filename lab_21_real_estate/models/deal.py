"""
Модуль модели сделки для системы управления недвижимостью.
Содержит класс Deal и enum'ы для типов и статусов сделок.
"""
from typing import Optional, Any

from database.types import DealType, DealStatus
from database.errors import ValidationError
from models.entity import Entity


class Deal(Entity):
    """
    Класс сделки - наследник абстрактного класса Entity.
    Представляет сделку купли-продажи или аренды недвижимости.
    """
    
    TABLE_NAME = 'deals'
    
    def __init__(
        self,
        id: Optional[int] = None,
        apartment_id: Optional[int] = None,
        client_id: Optional[int] = None,
        deal_type: DealType = DealType.SALE,
        deal_status: DealStatus = DealStatus.DRAFT,
        amount: float = 0.0,
        commission_rate: float = 2.0,
        deal_date: Optional[str] = None,
        notes: str = ""
    ) -> None:
        super().__init__(id, f"Сделка #{id}" if id else "Новая сделка")
        self.__apartment_id = apartment_id
        self.__client_id = client_id
        self.__deal_type = deal_type
        self.__deal_status = deal_status
        self.__amount = amount
        self.__commission_rate = commission_rate
        self.__deal_date = deal_date
        self.__notes = notes
    
    # Геттеры и сеттеры
    @property
    def apartment_id(self) -> Optional[int]:
        return self.__apartment_id
    
    @apartment_id.setter
    def apartment_id(self, value: int) -> None:
        if value is not None and value < 0:
            raise ValidationError("ID квартиры не может быть отрицательным", "apartment_id")
        self.__apartment_id = value
    
    @property
    def client_id(self) -> Optional[int]:
        return self.__client_id
    
    @client_id.setter
    def client_id(self, value: int) -> None:
        if value is not None and value < 0:
            raise ValidationError("ID клиента не может быть отрицательным", "client_id")
        self.__client_id = value
    
    @property
    def deal_type(self) -> DealType:
        return self.__deal_type
    
    @deal_type.setter
    def deal_type(self, value: DealType) -> None:
        self.__deal_type = value
    
    @property
    def deal_status(self) -> DealStatus:
        return self.__deal_status
    
    @deal_status.setter
    def deal_status(self, value: DealStatus) -> None:
        self.__deal_status = value
    
    @property
    def amount(self) -> float:
        return self.__amount
    
    @amount.setter
    def amount(self, value: float) -> None:
        if value < 0:
            raise ValidationError("Сумма не может быть отрицательной", "amount")
        self.__amount = value
    
    @property
    def commission_rate(self) -> float:
        return self.__commission_rate
    
    @commission_rate.setter
    def commission_rate(self, value: float) -> None:
        if value < 0 or value > 100:
            raise ValidationError("Комиссия должна быть от 0 до 100%", "commission_rate")
        self.__commission_rate = value
    
    @property
    def deal_date(self) -> Optional[str]:
        return self.__deal_date
    
    @deal_date.setter
    def deal_date(self, value: Optional[str]) -> None:
        self.__deal_date = value
    
    @property
    def notes(self) -> str:
        return self.__notes
    
    @notes.setter
    def notes(self, value: str) -> None:
        self.__notes = value[:500] if value else ""
    
    # Бизнес-методы
    def calculate_commission(self) -> float:
        """Расчет комиссии по сделке."""
        return round(self.__amount * self.__commission_rate / 100, 2)
    
    def calculate_net_amount(self) -> float:
        """Расчет суммы после вычета комиссии."""
        return round(self.__amount - self.calculate_commission(), 2)
    
    def activate(self) -> bool:
        """Активация сделки."""
        if self.__deal_status == DealStatus.DRAFT:
            self.__deal_status = DealStatus.ACTIVE
            return True
        return False
    
    def complete(self) -> bool:
        """Завершение сделки."""
        if self.__deal_status == DealStatus.ACTIVE:
            self.__deal_status = DealStatus.COMPLETED
            return True
        return False
    
    def cancel(self) -> bool:
        """Отмена сделки."""
        if self.__deal_status in (DealStatus.DRAFT, DealStatus.ACTIVE):
            self.__deal_status = DealStatus.CANCELLED
            return True
        return False
    
    def is_active(self) -> bool:
        """Проверка активности сделки."""
        return self.__deal_status == DealStatus.ACTIVE
    
    # Реализация абстрактных методов
    def get_info(self) -> str:
        """Формирование полной информации о сделке."""
        return (
            f"Сделка #{self.id or 'новая'}\n"
            f"Тип: {self.__deal_type.value}\n"
            f"Статус: {self.__deal_status.value}\n"
            f"ID квартиры: {self.__apartment_id or 'Не назначена'}\n"
            f"ID клиента: {self.__client_id or 'Не назначен'}\n"
            f"Сумма: {self.__amount:,.0f} руб.\n"
            f"Комиссия: {self.__commission_rate}% ({self.calculate_commission():,.0f} руб.)\n"
            f"Сумма после комиссии: {self.calculate_net_amount():,.0f} руб.\n"
            f"Дата: {self.__deal_date or 'Не назначена'}\n"
            f"Заметки: {self.__notes or 'Нет заметок'}"
        )
    
    def validate(self) -> bool:
        """Валидация данных сделки."""
        try:
            if not self.__apartment_id:
                raise ValidationError("Квартира обязательна", "apartment_id")
            if not self.__client_id:
                raise ValidationError("Клиент обязателен", "client_id")
            if self.__amount <= 0:
                raise ValidationError("Сумма должна быть положительной", "amount")
            if self.__commission_rate < 0 or self.__commission_rate > 100:
                raise ValidationError("Комиссия должна быть от 0 до 100%", "commission_rate")
            return True
        except ValidationError:
            return False
    
    def to_dict(self) -> dict[str, Any]:
        """Преобразование объекта в словарь."""
        data = super().to_dict()
        data.update({
            'apartment_id': self.__apartment_id,
            'client_id': self.__client_id,
            'deal_type': self.__deal_type.name,
            'deal_status': self.__deal_status.name,
            'amount': self.__amount,
            'commission_rate': self.__commission_rate,
            'deal_date': self.__deal_date,
            'notes': self.__notes
        })
        return data
