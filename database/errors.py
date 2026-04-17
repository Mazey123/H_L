class RealEstateError(Exception):
    """Базовое исключение для системы управления недвижимостью."""
    pass


class ValidationError(RealEstateError):
    """Исключение, возникающее при ошибке валидации данных."""
    
    def __init__(self, message: str, field: str | None = None):
        self.message = message
        self.field = field
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.field:
            return f"Ошибка валидации поля '{self.field}': {self.message}"
        return f"Ошибка валидации: {self.message}"


class DatabaseError(RealEstateError):
    """Исключение, возникающее при ошибке работы с базой данных."""
    
    def __init__(self, message: str, operation: str | None = None):
        self.message = message
        self.operation = operation
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.operation:
            return f"Ошибка БД ({self.operation}): {self.message}"
        return f"Ошибка БД: {self.message}"


class NotFoundError(RealEstateError):
    """Исключение, возникающее при отсутствии объекта в базе данных."""
    
    def __init__(self, entity_type: str, entity_id: int | None = None):
        self.entity_type = entity_type
        self.entity_id = entity_id
        if entity_id is not None:
            message = f"{entity_type} с ID {entity_id} не найден"
        else:
            message = f"{entity_type} не найден"
        super().__init__(message)
    
    def __str__(self) -> str:
        return self.args[0]


class BusinessLogicError(RealEstateError):
    """Исключение, возникающее при нарушении бизнес-логики."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"Ошибка бизнес-логики: {self.message}"
