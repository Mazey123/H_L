import os
from manager.real_estate_manager import RealEstateManager
from models.apartment import Apartment
from models.client import Client
from models.deal import Deal
from database.types import DealStatus

def menu():
    mgr = RealEstateManager("real_estate_demo.db")
    with open("database/schema.sql", "r") as f:
        mgr.init_db(f.read())   # на случай если БД нет

    while True:
        print("\n1. Квартиры\n2. Клиенты\n3. Сделки\n4. Выход")
        ch = input("Выбор: ")
        if ch == "1":
            print("1. Все  2. Добавить  3. Удалить")
            c = input()
            if c == "1":
                for a in mgr.get_all_apartments():
                    print(a.get_info())
            elif c == "2":
                a = Apartment()
                a.address = input("Адрес: ")
                a.city = input("Город: ")
                a.total_area = float(input("Площадь: "))
                a.rooms = int(input("Комнат: "))
                a.floor = int(input("Этаж: "))
                a.price = float(input("Цена: "))
                mgr.add_apartment(a)
                print("Добавлено")
            elif c == "3":
                mgr.delete_apartment(int(input("ID: ")))
                print("Удалено")
        elif ch == "2":
            print("1. Все  2. Добавить  3. Удалить")
            c = input()
            if c == "1":
                for cl in mgr.get_all_clients():
                    print(cl.get_info())
            elif c == "2":
                cl = Client(name=input("Имя: "), phone=input("Тел: "), email=input("Email: "))
                mgr.add_client(cl)
                print("Добавлен")
            elif c == "3":
                mgr.delete_client(int(input("ID: ")))
                print("Удалён")
        elif ch == "3":
            print("1. Все  2. Добавить  3. Изменить статус")
            c = input()
            if c == "1":
                for d in mgr.get_all_deals():
                    print(d.get_info())
            elif c == "2":
                d = Deal(apartment_id=int(input("ID кв: ")), client_id=int(input("ID клиента: ")), amount=float(input("Сумма: ")))
                mgr.add_deal(d)
                print("Добавлена")
            elif c == "3":
                did = int(input("ID сделки: "))
                d = mgr.get_deal(did)
                if d:
                    print("Статусы: HALF_ACTIVE, ACTIVE, COMPLETED")
                    new = input("Новый статус: ").upper()
                    if new in ["HALF_ACTIVE", "ACTIVE", "COMPLETED"]:
                        d.deal_status = DealStatus[new]
                        mgr.update_deal(d)
                        print("Обновлено")
                    else:
                        print("Неверно")
                else:
                    print("Не найдена")
        elif ch == "4":
            break

if __name__ == "__main__":
    menu()