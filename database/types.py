"""
Модуль типов и констант для системы управления недвижимостью.
"""
from enum import Enum
from typing import Optional


class DealType(Enum):
    """Типы сделок с недвижимостью."""
    SALE = "Продажа"
    RENT = "Аренда"
    LEASE = "Долгосрочная аренда"


class PropertyType(Enum):
    """Типы недвижимости."""
    APARTMENT = "Квартира"
    STUDIO = "Студия"
    PENTHOUSE = "Пентхаус"
    COMMERCIAL = "Коммерческая недвижимость"


class DealStatus(Enum):
    """Статусы сделок."""
    DRAFT = "Черновик"
    ACTIVE = "Активна"
    COMPLETED = "Завершена"
    CANCELLED = "Отменена"


# Константы для валидации
MIN_PRICE = 0
MAX_PRICE = 1_000_000_000
MIN_AREA = 10
MAX_AREA = 10000
MIN_ROOMS = 0
MAX_ROOMS = 20
MIN_FLOOR = 1
MAX_FLOOR = 100
