from enum import Enum
from typing import Optional


class DealType(Enum):
    """Типы сделок с недвижимостью."""
    SALE = "Продажа"
    RENT = "Аренда"
    Long_rent = "Долгосрочная аренда"


class PropertyType(Enum):
    """Типы недвижимости."""
    APARTMENT = "Квартира"
    STUDIO = "Студия"
    PENTHOUSE = "Пентхаус"


class DealStatus(Enum):
    """Статусы сделок."""
    HALF_ACTIVE = "Черновик"
    ACTIVE = "Активна"
    COMPLETED = "Завершена"
    CANCELLED = "Отменена"


# Константы для валидации
MIN_PRICE = 0
MAX_PRICE = 1_000_000_000
MIN_AREA = 0
MIN_ROOMS = 0
MAX_ROOMS = 20
MIN_FLOOR = 1
MAX_FLOOR = 20
