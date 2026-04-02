#!/usr/bin/env python3
"""
Демонстрационный скрипт для лабораторной работы №21
Тема: "Недвижимость (квартиры/сделки)"

Скрипт демонстрирует:
1. Создание экземпляров классов с использованием сеттеров
2. Вызов методов объектов (включая полиморфный get_info())
3. Работу менеджера: сохранение, загрузка, поиск по критериям
4. Обработку исключений при некорректных данных
"""
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.types import DealType, PropertyType, DealStatus
from database.errors import ValidationError, NotFoundError, DatabaseError
from models.apartment import Apartment
from models.client import Client
from models.deal import Deal
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
    
    # Инициализация менеджера и базы данных
    manager = RealEstateManager("real_estate_demo.db")
    
    # Загрузка схемы БД
    schema_path = os.path.join(os.path.dirname(__file__), "database", "schema.sql")
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    print_header("1. ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
    try:
        manager.init_database(schema_sql)
        print("✓ База данных успешно инициализирована")
    except DatabaseError as e:
        print(f"✗ Ошибка инициализации БД: {e}")
        return
    
    # ==================== ДЕМОНСТРАЦИЯ МОДЕЛЕЙ ====================
    print_separator("ЧАСТЬ 1: РАБОТА С МОДЕЛЯМИ (ООП)")
    
    print_header("1.1 Создание объектов Apartment через конструктор и сеттеры")
    apt1 = Apartment()
    apt1.address = "ул. Пушкина, д. 15, кв. 42"
    apt1.city = "Москва"
    apt1.district = "Центральный"
    apt1.total_area = 75.5
    apt1.living_area = 50.0
    apt1.rooms = 2
    apt1.floor = 7
    apt1.total_floors = 12
    apt1.price = 9500000.0
    apt1.property_type = PropertyType.APARTMENT
    apt1.description = "Уютная двухкомнатная квартира near метро"
    apt1.is_available = True
    print(f"✓ Квартира создана: {apt1.address}")
    
    apt2 = Apartment(
        address="пр. Ленина, д. 88, кв. 101",
        city="Санкт-Петербург",
        district="Невский",
        total_area=45.0,
        living_area=30.0,
        rooms=1,
        floor=10,
        total_floors=16,
        price=6200000.0,
        property_type=PropertyType.STUDIO,
        description="Светлая студия с видом на город"
    )
    print(f"✓ Квартира создана: {apt2.address}")
    
    print_header("1.2 Создание объектов Client")
    client1 = Client()
    client1.full_name = "Алексеев Алексей Алексеевич"
    client1.phone = "+7(999)111-22-33"
    client1.email = "alexeev@example.com"
    client1.passport_series = "4600"
    client1.passport_number = "654321"
    print(f"✓ Клиент создан: {client1.full_name}")
    
    client2 = Client(
        full_name="Борисова Бориса Борисовна",
        phone="+7(999)222-33-44",
        email="borisova@example.com"
    )
    print(f"✓ Клиент создан: {client2.full_name}")
    
    print_header("1.3 Демонстрация бизнес-методов Client")
    client1.add_bonus(100)
    print(f"✓ Начислено 100 бонусов. Текущий баланс: {client1.bonus_points}")
    
    client1.increment_deal_count()
    client1.increment_deal_count()
    client1.increment_deal_count()
    print(f"✓ Совершено сделок: {client1.deal_count}")
    print(f"✓ Статус клиента: {client1.get_client_status()}")
    print(f"✓ Скидка: {client1.get_discount_rate()}%")
    
    print_header("1.4 Создание объекта Deal")
    deal1 = Deal()
    deal1.apartment_id = 1  # Будет установлен после сохранения
    deal1.client_id = 1
    deal1.deal_type = DealType.SALE
    deal1.deal_status = DealStatus.DRAFT
    deal1.amount = 9500000.0
    deal1.commission_rate = 2.5
    deal1.deal_date = "2024-03-15"
    deal1.notes = "Предварительный договор купли-продажи"
    print("✓ Сделка создана")
    
    print_header("1.5 Полиморфизм: вызов метода get_info() для разных объектов")
    print("\n[Информация о квартире 1]:")
    print(apt1.get_info())
    
    print("\n[Информация о клиенте 1]:")
    print(client1.get_info())
    
    print("\n[Информация о сделке]:")
    print(deal1.get_info())
    
    print_header("1.6 Дополнительные бизнес-методы Apartment")
    print(f"✓ Стоимость за м²: {apt1.calculate_price_per_sqm():,.0f} руб.")
    print(f"✓ Находится на высоком этаже (≥10): {apt1.is_on_high_floor()}")
    print(f"✓ Тип квартиры: {apt1.get_room_type_description()}")
    
    print_header("1.7 Бизнес-методы Deal")
    print(f"✓ Комиссия по сделке: {deal1.calculate_commission():,.0f} руб.")
    print(f"✓ Сумма после комиссии: {deal1.calculate_net_amount():,.0f} руб.")
    
    # ==================== ОБРАБОТКА ИСКЛЮЧЕНИЙ ====================
    print_separator("ЧАСТЬ 2: ОБРАБОТКА ИСКЛЮЧЕНИЙ")
    
    print_header("2.1 Попытка создания квартиры с некорректными данными")
    try:
        bad_apt = Apartment()
        bad_apt.total_area = -50  # Некорректное значение
    except ValidationError as e:
        print(f"✓ Перехвачено исключение: {e}")
    
    print_header("2.2 Попытка валидации некорректного объекта")
    invalid_apt = Apartment(
        address="",  # Пустой адрес
        city="",     # Пустой город
        total_area=-10,
        rooms=2,
        floor=5,
        total_floors=10,
        price=5000000
    )
    is_valid = invalid_apt.validate()
    print(f"✓ Валидация вернула: {is_valid} (ожидалось False)")
    
    print_header("2.3 Попытка установки некорректного email клиенту")
    try:
        client1.email = "неправильный_email"
    except ValidationError as e:
        print(f"✓ Перехвачено исключение: {e}")
    
    # ==================== РАБОТА С БАЗОЙ ДАННЫХ ====================
    print_separator("ЧАСТЬ 3: РАБОТА С БАЗОЙ ДАННЫХ (МЕНЕДЖЕР)")
    
    print_header("3.1 Сохранение объектов в БД")
    try:
        apt1_id = manager.add_apartment(apt1)
        print(f"✓ Квартира 1 сохранена с ID: {apt1_id}")
        apt1.id = apt1_id
        
        apt2_id = manager.add_apartment(apt2)
        print(f"✓ Квартира 2 сохранена с ID: {apt2_id}")
        apt2.id = apt2_id
        
        client1_id = manager.add_client(client1)
        print(f"✓ Клиент 1 сохранен с ID: {client1_id}")
        client1.id = client1_id
        
        client2_id = manager.add_client(client2)
        print(f"✓ Клиент 2 сохранен с ID: {client2_id}")
        client2.id = client2_id
        
        # Обновляем ID в сделке
        deal1.apartment_id = apt1_id
        deal1.client_id = client1_id
        deal1_id = manager.add_deal(deal1)
        print(f"✓ Сделка сохранена с ID: {deal1_id}")
        deal1.id = deal1_id
        
    except ValidationError as e:
        print(f"✗ Ошибка валидации при сохранении: {e}")
    except DatabaseError as e:
        print(f"✗ Ошибка БД при сохранении: {e}")
    
    print_header("3.2 Загрузка объектов из БД по ID")
    try:
        loaded_apt = manager.get_apartment_by_id(apt1_id)
        print(f"✓ Загружена квартира: {loaded_apt.address}")
        print(f"  Цена: {loaded_apt.price:,.0f} руб.")
        
        loaded_client = manager.get_client_by_id(client1_id)
        print(f"✓ Загружен клиент: {loaded_client.full_name}")
        
        loaded_deal = manager.get_deal_by_id(deal1_id)
        print(f"✓ Загружена сделка #{loaded_deal.id}")
        print(f"  Тип: {loaded_deal.deal_type.value}, Статус: {loaded_deal.deal_status.value}")
        
    except NotFoundError as e:
        print(f"✗ Объект не найден: {e}")
    
    print_header("3.3 Получение всех объектов")
    all_apartments = manager.get_all_apartments()
    print(f"✓ Всего квартир в БД: {len(all_apartments)}")
    
    all_clients = manager.get_all_clients()
    print(f"✓ Всего клиентов в БД: {len(all_clients)}")
    
    all_deals = manager.get_all_deals()
    print(f"✓ Всего сделок в БД: {len(all_deals)}")
    
    print_header("3.4 Поиск квартир по критериям")
    found_apartments = manager.find_apartments_by_criteria(
        city="Москва",
        min_price=5000000,
        max_price=10000000,
        is_available=True
    )
    print(f"✓ Найдено квартир в Москве (5-10 млн руб.): {len(found_apartments)}")
    for apt in found_apartments:
        print(f"  - {apt.address}: {apt.price:,.0f} руб.")
    
    print_header("3.5 Поиск сделок по критериям")
    found_deals = manager.find_deals_by_criteria(
        deal_status=DealStatus.DRAFT
    )
    print(f"✓ Найдено сделок со статусом 'Черновик': {len(found_deals)}")
    
    print_header("3.6 Обновление объекта в БД")
    apt1.price = 9000000.0  # Изменяем цену
    updated = manager.update_apartment(apt1)
    print(f"✓ Квартира обновлена: {updated}")
    
    loaded_updated = manager.get_apartment_by_id(apt1_id)
    print(f"✓ Новая цена после загрузки: {loaded_updated.price:,.0f} руб.")
    
    print_header("3.7 Активация и завершение сделки")
    loaded_deal = manager.get_deal_by_id(deal1_id)
    activated = loaded_deal.activate()
    print(f"✓ Сделка активирована: {activated}")
    manager.update_deal(loaded_deal)
    
    completed = loaded_deal.complete()
    print(f"✓ Сделка завершена: {completed}")
    manager.update_deal(loaded_deal)
    
    final_deal = manager.get_deal_by_id(deal1_id)
    print(f"✓ Финальный статус сделки: {final_deal.deal_status.value}")
    
    # ==================== ЗАВЕРШЕНИЕ ====================
    print_separator("ЗАВЕРШЕНИЕ ДЕMONСТРАЦИИ")
    print("✓ Все этапы лабораторной работы выполнены успешно!")
    print("\nПродемонстрированы:")
    print("  • Абстрактный базовый класс Entity с приватными полями")
    print("  • Классы-наследники: Apartment, Client, Deal")
    print("  • Инкапсуляция через @property геттеры/сеттеры")
    print("  • Полиморфизм через метод get_info()")
    print("  • Абстрактные методы validate() и get_info()")
    print("  • Бизнес-методы в классах-наследниках")
    print("  • Класс-менеджер RealEstateManager с CRUD операциями")
    print("  • Интеграция с SQLite базой данных")
    print("  • Обработка исключений при некорректных данных")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
