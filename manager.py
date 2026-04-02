import sqlite3
from typing import List, Optional, Type, Union
from entities import Apartment, Client, Deal, Entity
from database import Database

class RealEstateManager:
    """Менеджер для работы с объектами недвижимости и базой данных."""

    def __init__(self, db: Database):
        self.db = db
        self._entity_map = {
            Apartment: ("apartments", self._row_to_apartment),
            Client: ("clients", self._row_to_client),
            Deal: ("deals", self._row_to_deal),
        }

    # ========== Вспомогательные методы преобразования ==========

    def _row_to_apartment(self, row: sqlite3.Row) -> Apartment:
        return Apartment(
            id=row["id"],
            title=row["title"],
            address=row["address"],
            area=row["area"],
            rooms=row["rooms"],
            price=row["price"]
        )

    def _row_to_client(self, row: sqlite3.Row) -> Client:
        return Client(
            id=row["id"],
            title=row["title"],
            phone=row["phone"],
            email=row["email"]
        )

    def _row_to_deal(self, row: sqlite3.Row) -> Deal:
        return Deal(
            id=row["id"],
            title=row["title"],
            apartment_id=row["apartment_id"],
            client_id=row["client_id"],
            deal_type=row["deal_type"],
            date=row["date"],
            amount=row["amount"]
        )

    # ========== Методы для квартир ==========

    def add_apartment(self, apartment: Apartment) -> bool:
        """Сохраняет новую квартиру в БД. Возвращает True при успехе."""
        if not apartment.validate():
            return False
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO apartments (title, address, area, rooms, price)
                VALUES (?, ?, ?, ?, ?)
            """, (apartment.title, apartment.address, apartment.area,
                  apartment.rooms, apartment.price))
            apartment.id = cursor.lastrowid
            conn.commit()
        return True

    def get_apartment_by_id(self, id: int) -> Optional[Apartment]:
        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM apartments WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_apartment(row)
        return None

    def get_all_apartments(self) -> List[Apartment]:
        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM apartments")
            rows = cursor.fetchall()
            return [self._row_to_apartment(row) for row in rows]

    def update_apartment(self, apartment: Apartment) -> bool:
        if not apartment.validate() or apartment.id is None:
            return False
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE apartments
                SET title=?, address=?, area=?, rooms=?, price=?
                WHERE id=?
            """, (apartment.title, apartment.address, apartment.area,
                  apartment.rooms, apartment.price, apartment.id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_apartment(self, id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM apartments WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0

    def find_apartments_by_criteria(self, max_price: float = None,
                                    min_rooms: int = None,
                                    min_area: float = None) -> List[Apartment]:
        """Поиск квартир по заданным критериям."""
        query = "SELECT * FROM apartments WHERE 1=1"
        params = []
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)
        if min_rooms is not None:
            query += " AND rooms >= ?"
            params.append(min_rooms)
        if min_area is not None:
            query += " AND area >= ?"
            params.append(min_area)

        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [self._row_to_apartment(row) for row in rows]

    # ========== Аналогичные методы для клиентов ==========

    def add_client(self, client: Client) -> bool:
        if not client.validate():
            return False
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clients (title, phone, email)
                VALUES (?, ?, ?)
            """, (client.title, client.phone, client.email))
            client.id = cursor.lastrowid
            conn.commit()
        return True

    def get_client_by_id(self, id: int) -> Optional[Client]:
        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_client(row)
        return None

    def get_all_clients(self) -> List[Client]:
        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients")
            rows = cursor.fetchall()
            return [self._row_to_client(row) for row in rows]

    def update_client(self, client: Client) -> bool:
        if not client.validate() or client.id is None:
            return False
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE clients
                SET title=?, phone=?, email=?
                WHERE id=?
            """, (client.title, client.phone, client.email, client.id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_client(self, id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0

    # ========== Методы для сделок ==========

    def add_deal(self, deal: Deal) -> bool:
        if not deal.validate():
            return False
        # Дополнительно проверим, что указанные apartment_id и client_id существуют
        if self.get_apartment_by_id(deal.apartment_id) is None:
            return False
        if self.get_client_by_id(deal.client_id) is None:
            return False

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO deals (title, apartment_id, client_id, deal_type, date, amount)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (deal.title, deal.apartment_id, deal.client_id,
                  deal.deal_type, deal.date, deal.amount))
            deal.id = cursor.lastrowid
            conn.commit()
        return True

    def get_deal_by_id(self, id: int) -> Optional[Deal]:
        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM deals WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_deal(row)
        return None

    def get_all_deals(self) -> List[Deal]:
        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM deals")
            rows = cursor.fetchall()
            return [self._row_to_deal(row) for row in rows]

    def update_deal(self, deal: Deal) -> bool:
        if not deal.validate() or deal.id is None:
            return False
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE deals
                SET title=?, apartment_id=?, client_id=?, deal_type=?, date=?, amount=?
                WHERE id=?
            """, (deal.title, deal.apartment_id, deal.client_id,
                  deal.deal_type, deal.date, deal.amount, deal.id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_deal(self, id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM deals WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0

    def find_deals_by_client(self, client_id: int) -> List[Deal]:
        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM deals WHERE client_id = ?", (client_id,))
            rows = cursor.fetchall()
            return [self._row_to_deal(row) for row in rows]