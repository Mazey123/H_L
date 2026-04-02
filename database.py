import sqlite3
from typing import Optional

class Database:
    """Класс для работы с базой данных SQLite."""
    def __init__(self, db_name: str = "real_estate.db"):
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self) -> None:
        """Создаёт таблицы, если они ещё не существуют."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Таблица квартир
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS apartments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    address TEXT NOT NULL,
                    area REAL NOT NULL,
                    rooms INTEGER NOT NULL,
                    price REAL NOT NULL
                )
            """)
            # Таблица клиентов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            """)
            # Таблица сделок
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS deals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    apartment_id INTEGER NOT NULL,
                    client_id INTEGER NOT NULL,
                    deal_type TEXT NOT NULL,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    FOREIGN KEY (apartment_id) REFERENCES apartments(id) ON DELETE CASCADE,
                    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def get_connection(self) -> sqlite3.Connection:
        """Возвращает соединение с БД."""
        return sqlite3.connect(self.db_name)