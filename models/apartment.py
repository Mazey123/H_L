from models.entity import Entity
from database.errors import ValidationError
from database.types import PropertyType

class Apartment(Entity):
    def __init__(self, id=None, address="", city="", total_area=0.0, rooms=0, floor=0, price=0.0, property_type=PropertyType.APARTMENT, is_available=True):
        super().__init__(id, address)
        self._address = address
        self._city = city
        self._total_area = total_area
        self._rooms = rooms
        self._floor = floor
        self._price = price
        self._property_type = property_type
        self._is_available = is_available

    @property
    def address(self): return self._address
    @address.setter
    def address(self, v): self._address = v

    @property
    def city(self): return self._city
    @city.setter
    def city(self, v): self._city = v

    @property
    def total_area(self): return self._total_area
    @total_area.setter
    def total_area(self, v): self._total_area = v

    @property
    def rooms(self): return self._rooms
    @rooms.setter
    def rooms(self, v): self._rooms = v

    @property
    def floor(self): return self._floor
    @floor.setter
    def floor(self, v): self._floor = v

    @property
    def price(self): return self._price
    @price.setter
    def price(self, v): self._price = v

    @property
    def property_type(self): return self._property_type
    @property_type.setter
    def property_type(self, v): self._property_type = v

    @property
    def is_available(self): return self._is_available
    @is_available.setter
    def is_available(self, v): self._is_available = v

    # бизнес-метод для отчёта
    def price_per_sqm(self):
        return self._price / self._total_area if self._total_area > 0 else 0
    
    def is_on_high_floor(self, threshold=10):
        return self._floor >= threshold

    def get_info(self):
        return f"Кв. {self._address}, {self._city}, {self._rooms}к, Этаж {self.floor}, {self._total_area}м², {self._price} руб."

    def validate(self):
        if not self._address:
            raise ValidationError("Нет адреса")
        if self._price <= 0:
            raise ValidationError("Цена <=0")
        return True