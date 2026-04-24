from typing import Optional, Any
from database.db_handler import DBHandler
from database.errors import NotFoundError, ValidationError
from database.types import DealType, PropertyType, DealStatus
from models.apartment import Apartment
from models.client import Client
from models.deal import Deal


class RealEstateManager:

    def __init__(self, db_path: str = "real_estate.db") -> None:
        """Инициализация менеджера с подключением к БД."""
        self._db = DBHandler(db_path)

    def init_database(self, schema_sql: str) -> None:
        """Инициализация схемы базы данных."""
        self._db.init_schema(schema_sql)

    #  Методы для Квартир

    def add_apartment(self, apartment: Apartment) -> int:
        """Добавление квартиры в базу данных."""
        if not apartment.validate():
            raise ValidationError("Данные квартиры не прошли валидацию")

        query = """
            INSERT INTO apartments (address, city, total_area,
                                   rooms, floor, price, property_type,
                                    is_available)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            apartment.address,
            apartment.city,
            apartment.total_area,
            apartment.rooms,
            apartment.floor,
            apartment.price,
            apartment.property_type.name,
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
            UPDATE apartments SET address=?, city=?, total_area=?,
                                  rooms=?, floor=?,
                                  price=?, property_type=?,
                                  is_available=?
            WHERE id=?
        """
        params = (
            apartment.address,
            apartment.city,
            apartment.total_area,
            apartment.rooms,
            apartment.floor,
            apartment.price,
            apartment.property_type.name,
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

    # Методы для Клиента

    def add_client(self, client: Client) -> int:
        """Добавление клиента в базу данных."""
        if not client.validate():
            raise ValidationError("Данные клиента не прошли валидацию")

        query = """
            INSERT INTO clients (full_name, phone, email)
            VALUES (?, ?, ?)
        """
        params = (
            client.full_name,
            client.phone,
            client.email,
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
            WHERE id=?
        """
        params = (
            client.full_name,
            client.phone,
            client.email,
            client.id
        )

        cursor = self._db.execute(query, params)
        return cursor.rowcount > 0

    def delete_client(self, client_id: int) -> bool:
        """Удаление клиента по ID."""
        query = "DELETE FROM clients WHERE id = ?"
        cursor = self._db.execute(query, (client_id,))
        return cursor.rowcount > 0

    #  Методы для сделок

    def add_deal(self, deal: Deal) -> int:
        """Добавление сделки в базу данных."""
        if not deal.validate():
            raise ValidationError("Данные сделки не прошли валидацию")

        query = """
            INSERT INTO deals (apartment_id, client_id, deal_type, deal_status,
                              amount)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (
            deal.apartment_id,
            deal.client_id,
            deal.deal_type.name,
            deal.deal_status.name,
            deal.amount,
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
                             amount=?
            WHERE id=?
        """
        params = (
            deal.apartment_id,
            deal.client_id,
            deal.deal_type.name,
            deal.deal_status.name,
            deal.amount,
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
            total_area=row['total_area'],
            rooms=row['rooms'],
            floor=row['floor'],
            price=row['price'],
            property_type=PropertyType[row['property_type']],
            is_available=bool(row['is_available'])
        )

    def _row_to_client(self, row: Any) -> Client:
        """Преобразование строки БД в объект Client."""
        client = Client(
            id=row['id'],
            full_name=row['full_name'],
            phone=row['phone'],
            email=row['email'] or "",
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
        )