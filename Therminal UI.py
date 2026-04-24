# simple_menu.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.types import DealStatus, PropertyType
from models import Apartment
from models import Client
from manager.real_estate_manager import RealEstateManager

# ---------- Вспомогательные функции ----------
def input_apartment() -> Apartment:
    """Ввод новой квартиры с клавиатуры."""
    print("\n--- Ввод новой квартиры ---")
    apt = Apartment()
    apt.address = input("Адрес: ")
    apt.city = input("Город: ")
    apt.total_area = float(input("Площадь (м²): "))
    apt.rooms = int(input("Количество комнат: "))
    apt.floor = int(input("Этаж: "))
    apt.price = float(input("Цена (руб): "))
    apt.property_type = PropertyType.APARTMENT
    apt.is_available = True
    return apt


def input_client() -> Client:
    """Ввод нового клиента с клавиатуры."""
    print("\n--- Ввод нового клиента ---")
    c = Client()
    c.full_name = input("ФИО: ")
    c.phone = input("Телефон: ")
    c.email = input("Email: ")
    return c


def print_all_apartments(manager: RealEstateManager):
    """Вывод всех квартир."""
    print("\n--- Список всех квартир ---")
    apartments = manager.get_all_apartments()
    if not apartments:
        print("В базе нет квартир.")
        return
    for apt in apartments:
        print(f"ID {apt.id}: {apt.address}, {apt.city} | {apt.rooms} к., {apt.total_area} м² | {apt.price:,.0f} руб.")


def print_all_clients(manager: RealEstateManager):
    """Вывод всех клиентов."""
    print("\n--- Список всех клиентов ---")
    clients = manager.get_all_clients()
    if not clients:
        print("В базе нет клиентов.")
        return
    for c in clients:
        print(f"ID {c.id}: {c.full_name} | Тел: {c.phone} | Email: {c.email} | Сделок: {c.deal_count}")

def change_price(manager: RealEstateManager):
    """Изменение цены квартиры по ID."""
    apt_id = int(input("Введите ID квартиры: "))
    new_price = float(input("Введите новую цену: "))
    apt = manager.get_apartment_by_id(apt_id)
    if apt is None:
        print("Квартира не найдена.")
        return
    apt.price = new_price
    manager.update_apartment(apt)
    print("Цена обновлена.")


def delete_apartment(manager: RealEstateManager):
    """Удаление квартиры по ID."""
    apt_id = int(input("Введите ID квартиры для удаления: "))
    success = manager.delete_apartment(apt_id)
    if success:
        print("Квартира удалена.")
    else:
        print("Удаление не выполнено (возможно, неверный ID).")

def delete_client(manager: RealEstateManager):
    """Удаление клиента по ID."""
    client_id = int(input("Введите ID клиента для удаления: "))
    success = manager.delete_client(client_id)
    if success:
        print("Клиент удален.")
    else:
        print("Удаление не выполнено (возможно, неверный ID).")


def change_deal_status(manager: RealEstateManager):
    """Изменение статуса сделки по ID."""
    deal_id = int(input("ID сделки: "))
    deal = manager.get_deal_by_id(deal_id)
    if deal is None:
        print("Сделка не найдена.")
        return
    print("Доступные статусы:")
    for status in DealStatus:
        print(f"  - {status.name}")
    status_str = input("Введите новый статус: ").upper()
    if status_str in DealStatus.__members__:
        deal.deal_status = DealStatus[status_str]
        manager.update_deal(deal)
        print("Статус обновлён.")
    else:
        print("Неверный статус.")



# ---------- Главное меню ----------
def simple_menu(manager: RealEstateManager):
    """Простое консольное меню для управления данными."""
    while True:
        print("\n" + "=" * 40)
        print("  ПРОСТОЕ МЕНЮ УПРАВЛЕНИЯ")
        print("=" * 40)
        print("1  - Показать все квартиры")
        print("2  - Добавить квартиру")
        print("3  - Изменить цену квартиры")
        print("4  - Удалить квартиру")
        print("5  - Показать всех клиентов")
        print("6  - Удалить клиента")
        print("7  - Добавить клиента")
        print("8  - Изменить статус сделки")
        print("0  - Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print_all_apartments(manager)
        elif choice == "2":
            apt = input_apartment()
            manager.add_apartment(apt)
            print("Квартира добавлена.")
        elif choice == "3":
            change_price(manager)
        elif choice == "4":
            delete_apartment(manager)
        elif choice == "5":
            print_all_clients(manager)
        elif choice == "6":
            delete_client(manager)
        elif choice == "7":
            client = input_client()
            manager.add_client(client)
            print("Клиент добавлен.")
        elif choice == "8":
            change_deal_status(manager)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


# ---------- Точка входа ----------
if __name__ == "__main__":
    # Инициализация базы данных (предполагаем, что она уже существует)
    db_path = "real_estate_demo.db"
    manager = RealEstateManager(db_path)

    # Проверяем наличие таблиц (инициализация схемы, если нужно)
    schema_path = os.path.join(os.path.dirname(__file__), "database", "schema.sql")
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        manager.init_database(schema_sql)
    else:
        print("Предупреждение: schema.sql не найден. Убедитесь, что таблицы существуют.")

    # Запуск меню
    simple_menu(manager)