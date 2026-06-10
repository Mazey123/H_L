from models.entity import Entity
from database.errors import ValidationError
from database.types import DealType, DealStatus

class Deal(Entity):
    def __init__(self, id=None, apartment_id=None, client_id=None, deal_type=DealType.SALE, deal_status=DealStatus.HALF_ACTIVE, amount=0.0):
        super().__init__(id, f"Сделка {id}")
        self._apartment_id = apartment_id
        self._client_id = client_id
        self._deal_type = deal_type
        self._deal_status = deal_status
        self._amount = amount

    @property
    def apartment_id(self): return self._apartment_id
    @apartment_id.setter
    def apartment_id(self, v): self._apartment_id = v

    @property
    def client_id(self): return self._client_id
    @client_id.setter
    def client_id(self, v): self._client_id = v

    @property
    def deal_type(self): return self._deal_type
    @deal_type.setter
    def deal_type(self, v): self._deal_type = v

    @property
    def deal_status(self): return self._deal_status
    @deal_status.setter
    def deal_status(self, v): self._deal_status = v

    @property
    def amount(self): return self._amount
    @amount.setter
    def amount(self, v): self._amount = v

    # два простых бизнес-метода
    def activate(self):
        if self._deal_status == DealStatus.HALF_ACTIVE:
            self._deal_status = DealStatus.ACTIVE
            return True
        return False

    def complete(self):
        if self._deal_status == DealStatus.ACTIVE:
            self._deal_status = DealStatus.COMPLETED
            return True
        return False

    def get_info(self):
        return f"Сделка {self.id}: кв.{self._apartment_id}, клиент {self._client_id}, {self._amount} руб., статус {self._deal_status.value}"

    def validate(self):
        if not self._apartment_id or not self._client_id:
            raise ValidationError("Не привязана квартира или клиент")
        if self._amount <= 0:
            raise ValidationError("Сумма <=0")
        return True