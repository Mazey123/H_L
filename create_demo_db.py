import os
from database.types import DealType, DealStatus
from models.apartment import Apartment
from models.client import Client
from models.deal import Deal
from manager.real_estate_manager import RealEstateManager

def init_demo(db_path="real_estate_demo.db"):
    if os.path.exists(db_path):
        os.remove(db_path)
    manager = RealEstateManager(db_path)
    with open("database/schema.sql", "r", encoding="utf-8") as f:
        manager.init_db(f.read())

    # квартиры
    a1 = Apartment(address="ул. Колотушкина 15", city="Сыктывкар", total_area=75, rooms=2, floor=12, price=9500000)
    a2 = Apartment(address="пр. Сушкина 88", city="Эжва", total_area=45, rooms=1, floor=10, price=6200000)
    a3 = Apartment(address="ул. Кукушкина 7", city="Максаковка", total_area=120, rooms=3, floor=5, price=12500000)
    manager.add_apartment(a1)
    manager.add_apartment(a2)
    manager.add_apartment(a3)

    # клиенты
    c1 = Client(name="Иван Тимушев", phone="+79991234567", email="ivan@mail.ru")
    c2 = Client(name="Даниил Саков", phone="+78887654321", email="danil@mail.ru")
    c3 = Client(name="Дмитрий Голубев", phone="+77771112233", email="dima@mail.ru")
    manager.add_client(c1)
    manager.add_client(c2)
    manager.add_client(c3)

    # сделки
    d1 = Deal(apartment_id=a1.id, client_id=c1.id, amount=9500000, deal_status=DealStatus.HALF_ACTIVE)
    d2 = Deal(apartment_id=a2.id, client_id=c2.id, amount=6200000, deal_status=DealStatus.ACTIVE)
    d3 = Deal(apartment_id=a3.id, client_id=c3.id, amount=12500000, deal_status=DealStatus.COMPLETED)
    manager.add_deal(d1)
    manager.add_deal(d2)
    manager.add_deal(d3)

    print("Demo database created.")
    return manager

if __name__ == "__main__":
    init_demo()