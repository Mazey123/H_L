from database import Database
from manager import RealEstateManager
from entities import Apartment, Client, Deal

def main():
    # Инициализация БД и менеджера
    db = Database()
    manager = RealEstateManager(db)

    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ СИСТЕМЫ 'НЕДВИЖИМОСТЬ'")
    print("=" * 50)

    # 1. Создание объектов с использованием сеттеров
    print("\n1. Создание объектов:")
    apt1 = Apartment(title="Уютная квартира в центре", address="ул. Ленина, 10", area=45.5, rooms=2, price=5500000)
    apt2 = Apartment(title="Просторная трёшка", address="пр. Мира, 25", area=85.0, rooms=3, price=8900000)

    client1 = Client(title="Иван Петров", phone="+7 999 123-45-67", email="ivan@example.com")
    client2 = Client(title="Мария Сидорова", phone="+7 911 987-65-43", email="maria@example.com")

    # 2. Вызов методов get_info() до сохранения
    print("\n2. Информация об объектах до сохранения:")
    print(apt1.get_info())
    print(client1.get_info())

    # 3. Сохранение объектов через менеджер
    print("\n3. Сохранение объектов в БД:")
    if manager.add_apartment(apt1):
        print(f"Квартира сохранена с ID: {apt1.id}")
    if manager.add_apartment(apt2):
        print(f"Квартира сохранена с ID: {apt2.id}")
    if manager.add_client(client1):
        print(f"Клиент сохранён с ID: {client1.id}")
    if manager.add_client(client2):
        print(f"Клиент сохранён с ID: {client2.id}")

    # 4. Создание сделки
    deal1 = Deal(title="Продажа квартиры Ивану", apartment_id=apt1.id, client_id=client1.id,
                 deal_type="sale", date="2026-03-12", amount=5500000)
    if manager.add_deal(deal1):
        print(f"Сделка сохранена с ID: {deal1.id}")

    # 5. Загрузка объектов из БД
    print("\n4. Загрузка объектов из БД по ID:")
    loaded_apt = manager.get_apartment_by_id(apt1.id)
    if loaded_apt:
        print(loaded_apt.get_info())

    loaded_client = manager.get_client_by_id(client1.id)
    if loaded_client:
        print(loaded_client.get_info())

    # 6. Поиск по критериям
    print("\n5. Поиск квартир дешевле 6 млн и с минимум 2 комнатами:")
    found = manager.find_apartments_by_criteria(max_price=6000000, min_rooms=2)
    for apt in found:
        print(f" - {apt.title}, цена: {apt.price} руб., комнат: {apt.rooms}")

    # 7. Демонстрация полиморфизма: get_info() для разных типов
    print("\n6. Полиморфный вызов get_info() для всех сущностей:")
    all_apartments = manager.get_all_apartments()
    all_clients = manager.get_all_clients()
    all_deals = manager.get_all_deals()
    for entity in all_apartments + all_clients + all_deals:
        print(entity.get_info())
        print("-" * 30)

    # 8. Обработка исключений: попытка создать объект с некорректными данными
    print("\n7. Обработка исключений (некорректные данные):")
    try:
        bad_apt = Apartment(title="", address="", area=-10, rooms=0, price=-100)
        if not bad_apt.validate():
            raise ValueError("Квартира содержит некорректные данные (отрицательная площадь и т.п.)")
    except ValueError as e:
        print(f"Ошибка: {e}")

    try:
        bad_client = Client(title="", phone="abc", email="notemail")
        if not bad_client.validate():
            raise ValueError("Клиент содержит некорректные данные (телефон, email)")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # 9. Удаление одной записи для демонстрации
    print("\n8. Удаление квартиры (ID = {})".format(apt2.id))
    if manager.delete_apartment(apt2.id):
        print("Квартира удалена.")
    else:
        print("Не удалось удалить квартиру.")

    print("\nДемонстрация завершена.")

if __name__ == "__main__":
    main()