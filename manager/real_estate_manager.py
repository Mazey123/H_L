#!/usr/bin/env python3
"""
Модуль менеджера для системы управления недвижимостью.
Обеспечивает взаимодействие с базой данных и объектами моделей.
"""
from typing import Optional, Any
from datetime import datetime

from database.db_handler import DBHandler
from database.errors import DatabaseError, NotFoundError, ValidationError
from database.types import DealType, PropertyType, DealStatus
from models.apartment import Apartment
from models.client import Client
from models.deal import Deal
from models.entity import Entity


class RealEstateManager:
    """
    Класс-менеджер для управления объектами недвижимости, клиентами и сделками.
    Реализует CRUD-операции и поиск по критериям.
    """

    def __init__(self, db_path: str = "real_estate.db") -> None:
        """Инициализация менеджера с подключением к БД."""
        self._db = DBHandler(db_path)

    def init_database(self, schema_sql: str) -> None:
        """Инициализация схемы базы данных."""
        self._db.init_schema(schema_sql)

    def clear_database(self) -> None:
        """Очистка всех таблиц базы данных (для тестов и демонстрации)."""
        # Удаляем данные в порядке, обратном созданию таблиц (из-за FK)
        self._db.execute("DELETE FROM deals", ())
        self._db.execute("DELETE FROM clients", ())
        self._db.execute("DELETE FROM apartments", ())

    # ==================== Методы для Apartment ====================

    def add_apartment(self, apartment: Apartment) -> int:
        """Добавление квартиры в базу данных."""
        if not apartment.validate():
            raise ValidationError("Данные квартиры не прошли валидацию")

        query = """
            INSERT INTO apartments (address, city, district, total_area, living_area,
                                   rooms, floor, total_floors, price, property_type,
                                   description, is_available)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            apartment.address,
            apartment.city,
            apartment.district,
            apartment.total_area,
            apartment.living_area,
            apartment.rooms,
            apartment.floor,
            apartment.total_floors,
            apartment.price,
            apartment.property_type.name,
            apartment.description,
            1 if apartment.is_available else 0
        )

        self._db.execute(query, params)
        new_id = self._db.get_last_insert_id()
        apartment.id = new_id
        return new_id

    def get_apartment_by_id(self, apartment_id: int) -> Apartment:
        """Получение квартиры по ID."""
        query = "SELECT * FROM apartments WHERE id = ?"
        row = self._db.fetchone(query, (apartment_id,))

        if not row:
            raise NotFoundError("Квартира", apartment_id)

        return self._row_to_apartment(row)

    def get_all_apartments(self) -> list[Apartment]:
        """Получение всех квартир."""
        query = "SELECT * FROM apartments ORDER BY created_at DESC"
        rows = self._db.fetchall(query)
        return [self._row_to_apartment(row) for row in rows]

    def update_apartment(self, apartment: Apartment) -> bool:
        """Обновление данных квартиры."""
        if not apartment.id:
            raise ValidationError("ID квартиры не установлен")
        if not apartment.validate():
            raise ValidationError("Данные квартиры не прошли валидацию")

        query = """
            UPDATE apartments SET address=?, city=?, district=?, total_area=?,
                                  living_area=?, rooms=?, floor=?, total_floors=?,
                                  price=?, property_type=?, description=?,
                                  is_available=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """
        params = (
            apartment.address,
            apartment.city,
            apartment.district,
            apartment.total_area,
            apartment.living_area,
            apartment.rooms,
            apartment.floor,
            apartment.total_floors,
            apartment.price,
            apartment.property_type.name,
            apartment.description,
            1 if apartment.is_available else 0,
            apartment.id
        )

        cursor = self._db.execute(query, params)
        return cursor.rowcount > 0

    def delete_apartment(self, apartment_id: int) -> bool:
        """Удаление квартиры по ID."""
        query = "DELETE FROM apartments WHERE id = ?"
        cursor = self._db.execute(query, (apartment_id,))
        return cursor.rowcount > 0

    def find_apartments_by_criteria(
        self,
        city: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rooms: Optional[int] = None,
        max_rooms: Optional[int] = None,
        is_available: Optional[bool] = None
    ) -> list[Apartment]:
        """Поиск квартир по критериям."""
        conditions = []
        params = []

        if city:
            conditions.append("city LIKE ?")
            params.append(f"%{city}%")

        if min_price is not None:
            conditions.append("price >= ?")
            params.append(min_price)

        if max_price is not None:
            conditions.append("price <= ?")
            params.append(max_price)

        if min_rooms is not None:
            conditions.append("rooms >= ?")
            params.append(min_rooms)

        if max_rooms is not None:
            conditions.append("rooms <= ?")
            params.append(max_rooms)

        if is_available is not None:
            conditions.append("is_available = ?")
            params.append(1 if is_available else 0)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        query = f"SELECT * FROM apartments WHERE {where_clause} ORDER BY price"

        rows = self._db.fetchall(query, tuple(params))
        return [self._row_to_apartment(row) for row in rows]

    # ==================== Методы для Client ====================

    def add_client(self, client: Client) -> int:
        """Добавление клиента в базу данных."""
        if not client.validate():
            raise ValidationError("Данные клиента не прошли валидацию")

        query = """
            INSERT INTO clients (full_name, phone, email, passport_series, passport_number)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (
            client.full_name,
            client.phone,
            client.email,
            client.passport_series,
            client.passport_number
        )

        self._db.execute(query, params)
        new_id = self._db.get_last_insert_id()
        client.id = new_id
        return new_id

    def get_client_by_id(self, client_id: int) -> Client:
        """Получение клиента по ID."""
        query = "SELECT * FROM clients WHERE id = ?"
        row = self._db.fetchone(query, (client_id,))

        if not row:
            raise NotFoundError("Клиент", client_id)

        return self._row_to_client(row)

    def get_all_clients(self) -> list[Client]:
        """Получение всех клиентов."""
        query = "SELECT * FROM clients ORDER BY created_at DESC"
        rows = self._db.fetchall(query)
        return [self._row_to_client(row) for row in rows]

    def update_client(self, client: Client) -> bool:
        """Обновление данных клиента."""
        if not client.id:
            raise ValidationError("ID клиента не установлен")
        if not client.validate():
            raise ValidationError("Данные клиента не прошли валидацию")

        query = """
            UPDATE clients SET full_name=?, phone=?, email=?,
                               passport_series=?, passport_number=?,
                               updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """
        params = (
            client.full_name,
            client.phone,
            client.email,
            client.passport_series,
            client.passport_number,
            client.id
        )

        cursor = self._db.execute(query, params)
        return cursor.rowcount > 0

    def delete_client(self, client_id: int) -> bool:
        """Удаление клиента по ID."""
        query = "DELETE FROM clients WHERE id = ?"
        cursor = self._db.execute(query, (client_id,))
        return cursor.rowcount > 0

    # ==================== Методы для Deal ====================

    def add_deal(self, deal: Deal) -> int:
        """Добавление сделки в базу данных."""
        if not deal.validate():
            raise ValidationError("Данные сделки не прошли валидацию")

        query = """
            INSERT INTO deals (apartment_id, client_id, deal_type, deal_status,
                              amount, commission_rate, deal_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            deal.apartment_id,
            deal.client_id,
            deal.deal_type.name,
            deal.deal_status.name,
            deal.amount,
            deal.commission_rate,
            deal.deal_date,
            deal.notes
        )

        self._db.execute(query, params)
        new_id = self._db.get_last_insert_id()
        deal.id = new_id
        return new_id

    def get_deal_by_id(self, deal_id: int) -> Deal:
        """Получение сделки по ID."""
        query = "SELECT * FROM deals WHERE id = ?"
        row = self._db.fetchone(query, (deal_id,))

        if not row:
            raise NotFoundError("Сделка", deal_id)

        return self._row_to_deal(row)

    def get_all_deals(self) -> list[Deal]:
        """Получение всех сделок."""
        query = "SELECT * FROM deals ORDER BY created_at DESC"
        rows = self._db.fetchall(query)
        return [self._row_to_deal(row) for row in rows]

    def update_deal(self, deal: Deal) -> bool:
        """Обновление данных сделки."""
        if not deal.id:
            raise ValidationError("ID сделки не установлен")
        if not deal.validate():
            raise ValidationError("Данные сделки не прошли валидацию")

        query = """
            UPDATE deals SET apartment_id=?, client_id=?, deal_type=?, deal_status=?,
                             amount=?, commission_rate=?, deal_date=?, notes=?,
                             updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """
        params = (
            deal.apartment_id,
            deal.client_id,
            deal.deal_type.name,
            deal.deal_status.name,
            deal.amount,
            deal.commission_rate,
            deal.deal_date,
            deal.notes,
            deal.id
        )

        cursor = self._db.execute(query, params)
        return cursor.rowcount > 0

    def delete_deal(self, deal_id: int) -> bool:
        """Удаление сделки по ID."""
        query = "DELETE FROM deals WHERE id = ?"
        cursor = self._db.execute(query, (deal_id,))
        return cursor.rowcount > 0

    def find_deals_by_criteria(
        self,
        deal_type: Optional[DealType] = None,
        deal_status: Optional[DealStatus] = None,
        client_id: Optional[int] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None
    ) -> list[Deal]:
        """Поиск сделок по критериям."""
        conditions = []
        params = []

        if deal_type:
            conditions.append("deal_type = ?")
            params.append(deal_type.name)

        if deal_status:
            conditions.append("deal_status = ?")
            params.append(deal_status.name)

        if client_id is not None:
            conditions.append("client_id = ?")
            params.append(client_id)

        if min_amount is not None:
            conditions.append("amount >= ?")
            params.append(min_amount)

        if max_amount is not None:
            conditions.append("amount <= ?")
            params.append(max_amount)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        query = f"SELECT * FROM deals WHERE {where_clause} ORDER BY amount DESC"

        rows = self._db.fetchall(query, tuple(params))
        return [self._row_to_deal(row) for row in rows]

    # ==================== Вспомогательные методы ====================

    def _row_to_apartment(self, row: Any) -> Apartment:
        """Преобразование строки БД в объект Apartment."""
        return Apartment(
            id=row['id'],
            address=row['address'],
            city=row['city'],
            district=row['district'] or "",
            total_area=row['total_area'],
            living_area=row['living_area'],
            rooms=row['rooms'],
            floor=row['floor'],
            total_floors=row['total_floors'],
            price=row['price'],
            property_type=PropertyType[row['property_type']],
            description=row['description'] or "",
            is_available=bool(row['is_available'])
        )

    def _row_to_client(self, row: Any) -> Client:
        """Преобразование строки БД в объект Client."""
        client = Client(
            id=row['id'],
            full_name=row['full_name'],
            phone=row['phone'],
            email=row['email'] or "",
            passport_series=row['passport_series'] or "",
            passport_number=row['passport_number'] or ""
        )
        # Примечание: bonus_points и deal_count не хранятся в БД в данной реализации
        return client

    def _row_to_deal(self, row: Any) -> Deal:
        """Преобразование строки БД в объект Deal."""
        return Deal(
            id=row['id'],
            apartment_id=row['apartment_id'],
            client_id=row['client_id'],
            deal_type=DealType[row['deal_type']],
            deal_status=DealStatus[row['deal_status']],
            amount=row['amount'],
            commission_rate=row['commission_rate'],
            deal_date=row['deal_date'],
            notes=row['notes'] or ""
        )

    def create_sample_data(self) -> dict[str, list[Any]]:
        """Создание тестовых данных для демонстрации."""
        results = {"apartments": [], "clients": [], "deals": []}

        # Создание квартир
        apts = [
            Apartment(
                address="ул. Пушкина, д. 15, кв. 42",
                city="Москва",
                district="Центральный",
                total_area=75.5,
                living_area=50.0,
                rooms=2,
                floor=7,
                total_floors=12,
                price=9500000.0,
                property_type=PropertyType.APARTMENT,
                description="Уютная квартира near метро"
            ),
            Apartment(
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
        ]

        for apt in apts:
            apt_id = self.add_apartment(apt)
            results["apartments"].append(apt)

        # Создание клиентов
        clients = [
            Client(
                full_name="Алексеев Алексей Алексеевич",
                phone="+7(999)111-22-33",
                email="alexeev@example.com",
                passport_series="4600",
                passport_number="654321"
            ),
            Client(
                full_name="Борисова Бориса Борисовна",
                phone="+7(999)222-33-44",
                email="borisova@example.com",
                passport_series="4601",
                passport_number="765432"
            )
        ]

        for client in clients:
            client_id = self.add_client(client)
            results["clients"].append(client)

        # Создание сделок
        if len(results["apartments"]) >= 1 and len(results["clients"]) >= 1:
            deal = Deal(
                apartment_id=results["apartments"][0].id,
                client_id=results["clients"][0].id,
                deal_type=DealType.SALE,
                deal_status=DealStatus.ACTIVE,
                amount=9500000.0,
                commission_rate=2.5,
                deal_date="2024-03-15",
                notes="Предварительный договор"
            )
            self.add_deal(deal)
            results["deals"].append(deal)

        return results