from models.entity import Entity
from database.errors import ValidationError

class Client(Entity):
    def __init__(
        self,
        id: int | None = None,
        full_name: str = "",
        phone: str = "",
        email: str = ""
    ) -> None:
        super().__init__(id, full_name)
        self.__full_name = full_name
        self.__phone = phone
        self.__email = email
        self.__deal_count: int = 0

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        if not value or len(value) > 100:
            raise ValidationError("ФИО должно быть от 1 до 100 символов", "full_name")
        self.__full_name = value

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str) -> None:
        if not value or len(value) > 20:
            raise ValidationError("Некорректный номер телефона", "phone")
        self.__phone = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        if value and '@' not in value:
            raise ValidationError("Некорректный email", "email")
        self.__email = value[:100] if value else ""

    @property
    def deal_count(self) -> int:
        return self.__deal_count

    def add_deal_count(self) -> None:
        self.__deal_count += 1

    def get_client_status(self) -> str:
        if self.__deal_count == 0:
            return "Новый"
        elif self.__deal_count <= 2:
            return "Постоянный"
        elif self.__deal_count <= 5:
            return "Лега"
        else:
            return "Откуда деньги?"

    def get_info(self) -> str:
        return (
            f"Клиент: {self.__full_name}\n"
            f"Телефон: {self.__phone}\n"
            f"Email: {self.__email or 'Не указан'}\n"
            f"Статус: {self.get_client_status()}"
        )

    def validate(self) -> bool:
        if not self.__full_name:
            raise ValidationError("ФИО обязательно", "full_name")
        if not self.__phone:
            raise ValidationError("Телефон обязателен", "phone")
        if self.__email and '@' not in self.__email:
            raise ValidationError("Некорректный email", "email")
        return True