import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.types import DealStatus
from database.errors import ValidationError
from models import Apartment
from manager.real_estate_manager import RealEstateManager


def print_separator(title: str = "") -> None:
    """Вывод разделителя."""
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)


def print_header(text: str) -> None:
    """Вывод заголовка."""
    print(f"\n--- {text} ---")


def main() -> None:
    """Основная функция демонстрации."""
    print_separator("ЛАБОРАТОРНАЯ РАБОТА №21: НЕДВИЖИМОСТЬ (КВАРТИРЫ/СДЕЛКИ)")
    print("Демонстрация принципов ООП: инкапсуляция, наследование, полиморфизм, абстракция")

    # Подключаемся к уже существующей базе данных
    manager = RealEstateManager("real_estate_demo.db")

    # Загрузка схемы для гарантии создания таблиц (если вдруг базы нет, но мы ожидаем, что она есть)
    schema_path = os.path.join(os.path.dirname(__file__), "database", "schema.sql")
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    print_header("1. ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
    manager.init_database(schema_sql)
    print(" База данных готова к работе")

    # Проверяем наличие данных в базе
    all_apartments = manager.get_all_apartments()
    all_clients = manager.get_all_clients()
    all_deals = manager.get_all_deals()

    if not all_apartments:
        print(" База данных пуста! Сначала запустите скрипт инициализации (create_demo_db.py).")
        return

    # Загружаем объекты для демонстрации (возьмём первые из каждой таблицы)
    apt1 = all_apartments[0]
    apt2 = all_apartments[1] if len(all_apartments) > 1 else None
    apt3 = all_apartments[2] if len(all_apartments) > 2 else None

    client1 = all_clients[0]
    client2 = all_clients[1] if len(all_clients) > 1 else None
    client3 = all_clients[2] if len(all_clients) > 2 else None

    deal1 = all_deals[0] if all_deals else None
    deal2 = all_deals[1] if len(all_deals) > 1 else None
    deal3 = all_deals[2] if len(all_deals) > 2 else None

    print_separator("ЧАСТЬ 1: РАБОТА С МОДЕЛЯМИ (ООП)")

    print_header("1.1 Информация о загруженных объектах")
    print(f" Квартира 1: {apt1.address}, {apt1.city}")
    if apt2:
        print(f" Квартира 2: {apt2.address}, {apt2.city}")
    if apt3:
        print(f" Квартира 3: {apt3.address}, {apt3.city}")
    print(f" Клиент 1: {client1.full_name}")
    if client2:
        print(f" Клиент 2: {client2.full_name}")
    if client3:
        print(f" Клиент 3: {client3.full_name}")
    if deal1:
        print(f" Сделка 1: ID={deal1.id}, сумма={deal1.amount:,.0f} руб., статус={deal1.deal_status.value}")
    if deal2:
        print(f" Сделка 2: ID={deal2.id}, сумма={deal2.amount:,.0f} руб., статус={deal2.deal_status.value}")
    if deal3:
        print(f" Сделка 3: ID={deal3.id}, сумма={deal3.amount:,.0f} руб., статус={deal3.deal_status.value}")

    print_header("1.2 Демонстрация бизнес-методов Client")
    a = 0
    while a != 7:
        print(f" Клиент {client3.full_name}: сделок = {client3.deal_count}, статус = {client3.get_client_status()}")
        a += 1
        client3.add_deal_count()

    print_header("1.3 Полиморфизм: вызов метода get_info() для разных объектов")
    print("\n[Информация о квартире 1]:")
    print(apt1.get_info())
    if apt2:
        print("\n[Информация о квартире 2]:")
        print(apt2.get_info())
    if apt3:
        print("\n[Информация о квартире 3]:")
        print(apt3.get_info())
    print("\n[Информация о клиенте 1]:")
    print(client1.get_info())
    if client2:
        print("\n[Информация о клиенте 2]:")
        print(client2.get_info())
    if client3:
        print("\n[Информация о клиенте 3]:")
        print(client3.get_info())
    if deal1:
        print("\n[Информация о сделке 1]:")
        print(deal1.get_info())
    if deal2:
        print("\n[Информация о сделке 2]:")
        print(deal2.get_info())
    if deal3:
        print("\n[Информация о сделке 3]:")
        print(deal3.get_info())

    print_header("1.4 Дополнительные бизнес-методы Apartment")
    print(f" Стоимость за 1м² квартиры 1: {apt1.calculate_price_per_sqm():,.0f} руб.")
    print(f" Находится на высоком этаже (≥10): {apt1.is_on_high_floor()}")
    print(f" Тип квартиры 1: {apt1.get_room_type_description()}")

    if deal1:
        print_header("1.5 Бизнес-методы Deal")
        print(f" Попытка завершить сделку 2: {deal2.complete()}")
        print(f" Попытка активировать сделку 1: {deal1.activate()}")

    print_separator("ЧАСТЬ 2: ОБРАБОТКА ИСКЛЮЧЕНИЙ")

    print_header("2.1 Попытка создания квартиры с некорректными данными")
    try:
        bad_apt = Apartment()
        bad_apt.total_area = -50
    except ValidationError as e:
        print(f" Перехвачено исключение: {e}")

    print_header("2.2 Попытка валидации некорректного объекта")
    invalid_apt = Apartment(
        address="",
        city="",
        total_area=-10,
        rooms=2,
        floor=5,
        price=5000000
    )
    try:
        invalid_apt.validate()
    except ValidationError as e:
        print(f" Перехвачено исключение: {e}")

    print_header("2.3 Попытка установки некорректного email клиенту")
    try:
        client1.email = "неправильный_email"
    except ValidationError as e:
        print(f" Перехвачено исключение: {e}")

    print_separator("ЧАСТЬ 3: РАБОТА С БАЗОЙ ДАННЫХ (МЕНЕДЖЕР)")

    print_header("3.1 Обновление объекта в БД")
    old_price = apt1.price
    apt1.price = 9000000.0
    updated = manager.update_apartment(apt1)
    print(f" Квартира обновлена: {updated}")
    loaded_updated = manager.get_apartment_by_id(apt1.id)
    print(f" Цена изменена с {old_price:,.0f} на {loaded_updated.price:,.0f} руб.")

    print_header("3.2 Поиск квартир по критериям")
    found_apartments = manager.find_apartments_by_criteria(
        city="Москва",
        min_price=5000000,
        max_price=10000000,
        is_available=True
    )
    print(f" Найдено квартир в Москве (5-10 млн руб.): {len(found_apartments)}")
    for apt in found_apartments:
        print(f"  - {apt.address}: {apt.price:,.0f} руб.")

    
    print_header("3.3 Поиск сделок по критериям")
    found_deals = manager.find_deals_by_criteria(
        deal_status=DealStatus.HALF_ACTIVE
    )
    print(f" Найдено сделок со статусом 'HALF_ACTIVE': {len(found_deals)}")

    print_header("3.4 Активация и завершение сделки")
    loaded_deal = manager.get_deal_by_id(deal1.id)
    activated = loaded_deal.activate()
    print(f" Сделка активирована: {activated}")
    manager.update_deal(loaded_deal)

    completed = loaded_deal.complete()
    print(f" Сделка завершена: {completed}")
    manager.update_deal(loaded_deal)

    final_deal = manager.get_deal_by_id(deal1.id)
    print(f" Финальный статус сделки: {final_deal.deal_status.value}")

if __name__ == "__main__":
    main()