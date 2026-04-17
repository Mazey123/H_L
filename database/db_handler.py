import sqlite3
from pathlib import Path
from typing import Optional, Any

from .errors import DatabaseError


class DBHandler:

    
    _instance: Optional['DBHandler'] = None
    _connection: Optional[sqlite3.Connection] = None

    def __init__(self, db_path: str = "real_estate.db"):
        """Инициализация подключения к базе данных."""
        if self._connection is None:
            self._db_path = db_path
            self._connect()
    
    def _connect(self) -> None:
        """Установление соединения с базой данных."""
        db_file = Path(self._db_path)
        self._connection = sqlite3.connect(
            str(db_file),
            check_same_thread=False,
            isolation_level=None
        )
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")

    
    @property
    def connection(self) -> sqlite3.Connection:
        """Получение активного соединения с БД."""
        if self._connection is None:
            self._connect()
        return self._connection  # type: ignore
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Выполнение SQL-запроса."""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor

    
    def executemany(self, query: str, params_list: list[tuple]) -> sqlite3.Cursor:
        """Выполнение SQL-запроса с множеством параметров."""

        cursor = self.connection.cursor()
        cursor.executemany(query, params_list)
        return cursor

    
    def fetchone(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Получение одной строки результата."""
        cursor = self.execute(query, params)
        return cursor.fetchone()
    
    def fetchall(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        """Получение всех строк результата."""
        cursor = self.execute(query, params)
        return cursor.fetchall()
    
    def get_last_insert_id(self) -> int:
        """Получение ID последней вставленной записи."""
        cursor = self.execute("SELECT last_insert_rowid()")
        result = cursor.fetchone()
        return result[0] if result else 0
    
    def begin_transaction(self) -> None:
        """Начало транзакции."""
        self.connection.execute("BEGIN")
    
    def commit(self) -> None:
        """Фиксация транзакции."""

        self.connection.commit()

    
    def rollback(self) -> None:
        """Откат транзакции."""

        self.connection.rollback()

    def close(self) -> None:
        """Закрытие соединения с базой данных."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def init_schema(self, schema_sql: str) -> None:
        """Инициализация схемы базы данных из SQL-файла."""
        # Разделяем по точкам с запятой, но учитываем многострочные запросы
        statements = []
        current_statement = []
        
        for line in schema_sql.split('\n'):
            line = line.strip()
            # Пропускаем комментарии и пустые строки
            if not line or line.startswith('--'):
                continue
            current_statement.append(line)
            
            # Если строка заканчивается на ';', завершаем оператор
            if line.endswith(';'):
                statements.append(' '.join(current_statement))
                current_statement = []
        
        # Добавляем последний оператор если есть
        if current_statement:
            last_stmt = ' '.join(current_statement).strip()
            if last_stmt and not last_stmt.startswith('--'):
                statements.append(last_stmt)
        
        for statement in statements:
            statement = statement.strip()
            if statement:
                self.execute(statement)
        self.commit()

