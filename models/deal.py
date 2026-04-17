from typing import Optional, Any

from database.types import DealType, DealStatus
from database.errors import ValidationError
from models.entity import Entity


class Deal(Entity):

    
    TABLE_NAME = 'deals'
    
    def __init__(
        self,
        id: Optional[int] = None,
        apartment_id: Optional[int] = None,
        client_id: Optional[int] = None,
        deal_type: DealType = DealType.SALE,
        deal_status: DealStatus = DealStatus.HALF_ACTIVE,
        amount: float = 0.0,
    ) -> None:
        super().__init__(id, f"Сделка #{id}" if id else "Новая сделка")
        self.__apartment_id = apartment_id
        self.__client_id = client_id
        self.__deal_type = deal_type
        self.__deal_status = deal_status
        self.__amount = amount
    
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

    # Бизнес-методы
    
    def activate(self) -> bool:
        """Переход в активную стадию сделки."""
        if self.__deal_status == DealStatus.HALF_ACTIVE:
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
            f"Сделка {self.id or 'новая'}\n"
            f"Тип: {self.__deal_type.value}\n"
            f"Статус: {self.__deal_status.value}\n"
            f"ID квартиры: {self.__apartment_id or 'Не назначена'}\n"
            f"ID клиента: {self.__client_id or 'Не назначен'}\n"
            f"Сумма: {self.__amount:,.0f} руб.\n"
        )
    
    def validate(self) -> bool:
        """Валидация данных сделки."""
        if not self.__apartment_id:
            raise ValidationError("Квартира обязательна", "apartment_id")
        if not self.__client_id:
            raise ValidationError("Клиент обязателен", "client_id")
        if self.__amount <= 0:
            raise ValidationError("Сумма должна быть положительной", "amount")
        return True
    
    def to_dict(self) -> dict[str, Any]:
        """Преобразование объекта в словарь."""
        data = super().to_dict()
        data.update({
            'apartment_id': self.__apartment_id,
            'client_id': self.__client_id,
            'deal_type': self.__deal_type.name,
            'deal_status': self.__deal_status.name,
            'amount': self.__amount,
        })
        return data
