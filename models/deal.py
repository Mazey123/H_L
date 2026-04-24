from models.entity import Entity
from database.errors import ValidationError
from database.types import DealType, DealStatus

class Deal(Entity):
    def __init__(
        self,
        id: int | None = None,
        apartment_id: int | None = None,
        client_id: int | None = None,
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

    @property
    def apartment_id(self) -> int | None:
        return self.__apartment_id

    @apartment_id.setter
    def apartment_id(self, value: int) -> None:
        if value is not None and value < 0:
            raise ValidationError("ID квартиры не может быть отрицательным", "apartment_id")
        self.__apartment_id = value

    @property
    def client_id(self) -> int | None:
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

    def activate(self) -> bool:
        if self.__deal_status == DealStatus.HALF_ACTIVE:
            self.__deal_status = DealStatus.ACTIVE
            return True
        return False

    def complete(self) -> bool:
        if self.__deal_status == DealStatus.ACTIVE:
            self.__deal_status = DealStatus.COMPLETED
            return True
        return False

    def cancel(self) -> bool:
        if self.__deal_status in (DealStatus.HALF_ACTIVE, DealStatus.ACTIVE):
            self.__deal_status = DealStatus.CANCELLED
            return True
        return False

    def is_active(self) -> bool:
        return self.__deal_status == DealStatus.ACTIVE

    def get_info(self) -> str:
        return (
            f"Сделка {self.id or 'новая'}\n"
            f"Тип: {self.__deal_type.value}\n"
            f"Статус: {self.__deal_status.value}\n"
            f"ID квартиры: {self.__apartment_id or 'Не назначена'}\n"
            f"ID клиента: {self.__client_id or 'Не назначен'}\n"
            f"Сумма: {self.__amount:,.0f} руб."
        )

    def validate(self) -> bool:
        if not self.__apartment_id:
            raise ValidationError("Квартира обязательна", "apartment_id")
        if not self.__client_id:
            raise ValidationError("Клиент обязателен", "client_id")
        if self.__amount <= 0:
            raise ValidationError("Сумма должна быть положительной", "amount")
        return True