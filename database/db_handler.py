import sqlite3

class DBHandler:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def execute(self, query: str, params=()):
        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur

    def executescript(self, script: str):
        self.conn.executescript(script)  

    def fetchone(self, query: str, params=()):
        cur = self.execute(query, params)
        return cur.fetchone()

    def fetchall(self, query: str, params=()):
        cur = self.execute(query, params)
        return cur.fetchall()

    def get_last_id(self):
        return self.execute("SELECT last_insert_rowid()").fetchone()[0]

    def close(self):
        self.conn.close()