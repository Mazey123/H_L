from models.entity import Entity
from database.errors import ValidationError
from database.types import PropertyType, MIN_PRICE, MAX_PRICE, MIN_AREA, MIN_ROOMS, MAX_ROOMS, MIN_FLOOR, MAX_FLOOR

class Apartment(Entity):
    def __init__(
        self,
        id: int | None = None,
        address: str = "",
        city: str = "",
        total_area: float = 0.0,
        rooms: int = 1,
        floor: int = 1,
        price: float = 0.0,
        property_type: PropertyType = PropertyType.APARTMENT,
        is_available: bool = True
    ) -> None:
        super().__init__(id, f"Квартира {address}")
        self.__address = address
        self.__city = city
        self.__total_area = total_area
        self.__rooms = rooms
        self.__floor = floor
        self.__price = price
        self.__property_type = property_type
        self.__is_available = is_available

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str) -> None:
        if not value or len(value) > 100:
            raise ValidationError("Адрес должен быть от 1 до 100 символов", "address")
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
    def total_area(self) -> float:
        return self.__total_area

    @total_area.setter
    def total_area(self, value: float) -> None:
        if value <= MIN_AREA:
            raise ValidationError("Площадь должна быть положительной", "total_area")
        self.__total_area = value

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
    def is_available(self) -> bool:
        return self.__is_available

    @is_available.setter
    def is_available(self, value: bool) -> None:
        self.__is_available = value

    def calculate_price_per_sqm(self) -> float:
        if self.__total_area <= 0:
            return 0.0
        return round(self.__price / self.__total_area, 2)

    def is_on_high_floor(self, threshold: int = 10) -> bool:
        return self.__floor >= threshold

    def get_room_type_description(self) -> str:
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

    def get_info(self) -> str:
        status = "В продаже" if self.__is_available else "Продана"
        return (
            f"Адрес: {self.__city}, {self.__address}\n"
            f"Площадь: {self.__total_area} м²\n"
            f"Этаж: {self.__floor}\n"
            f"Тип: {self.__property_type.value}\n"
            f"Цена: {self.__price:,.0f} руб. ({self.calculate_price_per_sqm():,.0f} руб./м²)\n"
            f"Статус: {status}"
        )

    def validate(self) -> bool:
        if not self.__address:
            raise ValidationError("Адрес обязателен", "address")
        if not self.__city:
            raise ValidationError("Город обязателен", "city")
        if self.__total_area <= 0:
            raise ValidationError("Площадь должна быть положительной", "total_area")
        if self.__price < 0:
            raise ValidationError("Цена не может быть отрицательной", "price")
        return True