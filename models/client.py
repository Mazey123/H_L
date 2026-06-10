from models.entity import Entity
from database.errors import ValidationError

class Client(Entity):
    def __init__(self, id=None, name="", phone="", email=""):
        super().__init__(id, name)
        self._name = name
        self._phone = phone
        self._email = email

    @property
    def name(self): return self._name
    @name.setter
    def name(self, v): self._name = v

    @property
    def phone(self): return self._phone
    @phone.setter
    def phone(self, v): self._phone = v

    @property
    def email(self): return self._email
    @email.setter
    def email(self, v): self._email = v

    # простой бизнес-метод
    def has_phone(self):
        return bool(self._phone)

    def get_info(self):
        return f"Клиент {self._name}, тел:{self._phone}, email:{self._email}"

    def validate(self):
        if not self._name:
            raise ValidationError("Имя пустое")
        return True