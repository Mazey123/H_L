"""
Модуль модели квартиры для системы управления недвижимостью.
"""
from typing import Optional, Any

from database.types import (
    PropertyType,
    MIN_PRICE, MAX_PRICE, MIN_AREA, MAX_AREA,
    MIN_ROOMS, MAX_ROOMS, MIN_FLOOR, MAX_FLOOR
)
from database.errors import ValidationError
from models.entity import Entity


class Apartment(Entity):
    """
    Класс квартиры - наследник абстрактного класса Entity.
    Представляет объект недвижимости.
    """
    
    TABLE_NAME = 'apartments'
    
    def __init__(
        self,
        id: Optional[int] = None,
        address: str = "",
        city: str = "",
        district: str = "",
        total_area: float = 0.0,
        living_area: Optional[float] = None,
        rooms: int = 1,
        floor: int = 1,
        total_floors: int = 1,
        price: float = 0.0,
        property_type: PropertyType = PropertyType.APARTMENT,
        description: str = "",
        is_available: bool = True
    ) -> None:
        super().__init__(id, f"Квартира {address}")
        self.__address = address
        self.__city = city
        self.__district = district
        self.__total_area = total_area
        self.__living_area = living_area
        self.__rooms = rooms
        self.__floor = floor
        self.__total_floors = total_floors
        self.__price = price
        self.__property_type = property_type
        self.__description = description
        self.__is_available = is_available
    
    # Геттеры и сеттеры для приватных атрибутов
    @property
    def address(self) -> str:
        return self.__address
    
    @address.setter
    def address(self, value: str) -> None:
        if not value or len(value) > 255:
            raise ValidationError("Адрес должен быть от 1 до 255 символов", "address")
        self.__address = value
    
    @property
    def city(self) -> str:
        return self.__city
    
    @city.setter
    def city(self, value: str) -> None:
        if not value or len(value) > 100:
            raise ValidationError("Город должен быть от 1 до 100 символов", "city")
        self.__city = value
    
    @property
    def district(self) -> str:
        return self.__district
    
    @district.setter
    def district(self, value: str) -> None:
        self.__district = value[:100] if value else ""
    
    @property
    def total_area(self) -> float:
        return self.__total_area
    
    @total_area.setter
    def total_area(self, value: float) -> None:
        if not (MIN_AREA <= value <= MAX_AREA):
            raise ValidationError(f"Общая площадь должна быть от {MIN_AREA} до {MAX_AREA} м²", "total_area")
        self.__total_area = value
    
    @property
    def living_area(self) -> Optional[float]:
        return self.__living_area
    
    @living_area.setter
    def living_area(self, value: Optional[float]) -> None:
        if value is not None and value <= 0:
            raise ValidationError("Жилая площадь должна быть положительной", "living_area")
        self.__living_area = value
    
    @property
    def rooms(self) -> int:
        return self.__rooms
    
    @rooms.setter
    def rooms(self, value: int) -> None:
        if not (MIN_ROOMS <= value <= MAX_ROOMS):
            raise ValidationError(f"Количество комнат должно быть от {MIN_ROOMS} до {MAX_ROOMS}", "rooms")
        self.__rooms = value
    
    @property
    def floor(self) -> int:
        return self.__floor
    
    @floor.setter
    def floor(self, value: int) -> None:
        if not (MIN_FLOOR <= value <= MAX_FLOOR):
            raise ValidationError(f"Этаж должен быть от {MIN_FLOOR} до {MAX_FLOOR}", "floor")
        self.__floor = value
    
    @property
    def total_floors(self) -> int:
        return self.__total_floors
    
    @total_floors.setter
    def total_floors(self, value: int) -> None:
        if not (MIN_FLOOR <= value <= MAX_FLOOR):
            raise ValidationError(f"Общее количество этажей должно быть от {MIN_FLOOR} до {MAX_FLOOR}", "total_floors")
        self.__total_floors = value
    
    @property
    def price(self) -> float:
        return self.__price
    
    @price.setter
    def price(self, value: float) -> None:
        if not (MIN_PRICE <= value <= MAX_PRICE):
            raise ValidationError(f"Цена должна быть от {MIN_PRICE} до {MAX_PRICE}", "price")
        self.__price = value
    
    @property
    def property_type(self) -> PropertyType:
        return self.__property_type
    
    @property_type.setter
    def property_type(self, value: PropertyType) -> None:
        self.__property_type = value
    
    @property
    def description(self) -> str:
        return self.__description
    
    @description.setter
    def description(self, value: str) -> None:
        self.__description = value[:1000] if value else ""
    
    @property
    def is_available(self) -> bool:
        return self.__is_available
    
    @is_available.setter
    def is_available(self, value: bool) -> None:
        self.__is_available = value
    
    # Бизнес-методы
    def calculate_price_per_sqm(self) -> float:
        """Расчет стоимости за квадратный метр."""
        if self.__total_area <= 0:
            return 0.0
        return round(self.__price / self.__total_area, 2)
    
    def is_on_high_floor(self, threshold: int = 10) -> bool:
        """Проверка, находится ли квартира на высоком этаже."""
        return self.__floor >= threshold
    
    def get_room_type_description(self) -> str:
        """Получение описания типа квартиры по количеству комнат."""
        if self.__rooms == 0:
            return "Студия"
        elif self.__rooms == 1:
            return "Однокомнатная"
        elif self.__rooms == 2:
            return "Двухкомнатная"
        elif self.__rooms == 3:
            return "Трехкомнатная"
        else:
            return f"Многокомнатная ({self.__rooms} комн.)"
    
    # Реализация абстрактных методов
    def get_info(self) -> str:
        """Формирование полной информации о квартире."""
        status = "В продаже" if self.__is_available else "Продана"
        return (
            f"{self.get_room_type_description()} квартира\n"
            f"Адрес: {self.__city}, {self.__address}\n"
            f"Район: {self.__district}\n"
            f"Площадь: {self.__total_area} м² (жилая: {self.__living_area or 'н/д'} м²)\n"
            f"Этаж: {self.__floor}/{self.__total_floors}\n"
            f"Тип: {self.__property_type.value}\n"
            f"Цена: {self.__price:,.0f} руб. ({self.calculate_price_per_sqm():,.0f} руб./м²)\n"
            f"Статус: {status}\n"
            f"Описание: {self.__description or 'Нет описания'}"
        )
    
    def validate(self) -> bool:
        """Валидация данных квартиры."""
        try:
            if not self.__address:
                raise ValidationError("Адрес обязателен", "address")
            if not self.__city:
                raise ValidationError("Город обязателен", "city")
            if self.__total_area <= 0:
                raise ValidationError("Площадь должна быть положительной", "total_area")
            if self.__living_area and self.__living_area > self.__total_area:
                raise ValidationError("Жилая площадь не может превышать общую", "living_area")
            if self.__price < 0:
                raise ValidationError("Цена не может быть отрицательной", "price")
            if self.__floor > self.__total_floors:
                raise ValidationError("Этаж не может превышать общее количество этажей", "floor")
            return True
        except ValidationError:
            return False
    
    def to_dict(self) -> dict[str, Any]:
        """Преобразование объекта в словарь."""
        data = super().to_dict()
        data.update({
            'address': self.__address,
            'city': self.__city,
            'district': self.__district,
            'total_area': self.__total_area,
            'living_area': self.__living_area,
            'rooms': self.__rooms,
            'floor': self.__floor,
            'total_floors': self.__total_floors,
            'price': self.__price,
            'property_type': self.__property_type.name,
            'description': self.__description,
            'is_available': self.__is_available
        })
        return data
