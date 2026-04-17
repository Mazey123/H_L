import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.types import DealType, PropertyType, DealStatus
from models.apartment import Apartment
from models.client import Client
from models.deal import Deal
from manager.real_estate_manager import RealEstateManager


def create_demo_data(manager: RealEstateManager) -> dict:
    """
    Заполняет базу данных демонстрационными объектами.
    Возвращает словарь с созданными объектами.
    """
    # Создаём объекты в памяти
    apt1 = Apartment()
    apt1.address = "ул. Пушкина, д. 15, кв. 42"
    apt1.city = "Москва"
    apt1.total_area = 75.5
    apt1.rooms = 2
    apt1.floor = 12
    apt1.price = 9500000.0
    apt1.property_type = PropertyType.APARTMENT
    apt1.is_available = True

    apt2 = Apartment(
        address="пр. Ленина, д. 88, кв. 101",
        city="Санкт-Петербург",
        total_area=45.0,
        rooms=1,
        floor=10,
        price=6200000.0,
        property_type=PropertyType.STUDIO
    )

    apt3 = Apartment(
        address="ул. Мича-Яг, д. 7, кв. 2",
        city = "Верхняя Максаковка",
        total_area = 999999,
        rooms = 9999,
        floor = 1,
        price = 9999999999.0,
        property_type=PropertyType.PENTHOUSE
    )

    client1 = Client()
    client1.full_name = "Алексеев Алексей Алексеевич"
    client1.phone = "+7(999)111-22-33"
    client1.email = "alexeev@example.com"

    client2 = Client(
        full_name="Борисова Бориса Борисовна",
        phone="+7(999)222-33-44",
        email="borisova@example.com"
    )

    client3 = Client()
    client3.full_name = "Голубев Дмитрий Евгеньевич"
    client3.phone = "8(904)867-44-58"
    client3.email = "golubev.dima2005@mail.ru"

    # Сохраняем в БД
    apt1_id = manager.add_apartment(apt1)
    apt1.id = apt1_id
    print(f" Квартира 1 сохранена с ID: {apt1_id}")

    apt2_id = manager.add_apartment(apt2)
    apt2.id = apt2_id
    print(f" Квартира 2 сохранена с ID: {apt2_id}")

    apt3_id = manager.add_apartment(apt3)
    apt3.id = apt3_id
    print(f" Квартира 3 сохранена с ID: {apt3_id}")

    client1_id = manager.add_client(client1)
    client1.id = client1_id
    print(f" Клиент 1 сохранён с ID: {client1_id}")

    client2_id = manager.add_client(client2)
    client2.id = client2_id
    print(f" Клиент 2 сохранён с ID: {client2_id}")

    client3_id = manager.add_client(client3)
    client3.id = client3_id
    print(f" Клиент 3 сохранён с ID: {client3_id}")


    deal1 = Deal()
    deal1.apartment_id = apt1_id
    deal1.client_id = client1_id
    deal1.deal_type = DealType.SALE
    deal1.deal_status = DealStatus.HALF_ACTIVE
    deal1.amount = 9500000.0

    deal2 = Deal()
    deal2.apartment_id = apt2_id
    deal2.client_id = client2_id
    deal2.deal_type = DealType.SALE
    deal2.deal_status = DealStatus.ACTIVE
    deal2.amount = 1000000.0

    deal3 = Deal()
    deal3.apartment_id = apt3_id
    deal3.client_id = client3_id
    deal3.deal_type = DealType.SALE
    deal3.deal_status = DealStatus.COMPLETED
    deal3.amount = 99999999.0

    deal1_id = manager.add_deal(deal1)
    deal1.id = deal1_id
    print(f" Сделка сохранена с ID: {deal1_id}")
    
    deal2_id = manager.add_deal(deal2)
    deal2.id = deal2_id
    print(f" Сделка сохранена с ID: {deal2_id}")

    deal3_id = manager.add_deal(deal3)
    deal3.id = deal3_id
    print(f" Сделка сохранена с ID: {deal3_id}")

    
    return {
        'apt1': apt1,
        'apt2': apt2,
        'apt3': apt3,
        'client1': client1,
        'client2': client2,
        'client3': client3,
        'deal1': deal1,
        'deal2': deal2,
        'deal3': deal3
    }


def init_demo_database(db_path: str = "real_estate_demo.db") -> None:

    if os.path.exists(db_path):
        os.remove(db_path)
        print(f" Старая база '{db_path}' удалена.")

    manager = RealEstateManager(db_path)

    schema_path = os.path.join(os.path.dirname(__file__), "database", "schema.sql")
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    manager.init_database(schema_sql)

    create_demo_data(manager)


if __name__ == "__main__":
    init_demo_database()