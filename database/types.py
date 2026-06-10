from enum import Enum

class DealType(Enum):
    SALE = "Продажа"

class PropertyType(Enum):
    APARTMENT = "Квартира"

class DealStatus(Enum):
    HALF_ACTIVE = "Черновик"
    ACTIVE = "Активна"
    COMPLETED = "Завершена"