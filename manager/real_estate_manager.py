from database.db_handler import DBHandler
from database.types import PropertyType, DealType, DealStatus
from models.apartment import Apartment
from models.client import Client
from models.deal import Deal

class RealEstateManager:
    def __init__(self, db_path):
        self.db = DBHandler(db_path)

    def init_db(self, schema_sql):
        self.db.executescript(schema_sql)
        self.db.conn.commit()

    # ---------- Apartment ----------
    def add_apartment(self, apt):
        sql = "INSERT INTO apartments (address,city,total_area,rooms,floor,price,property_type,is_available) VALUES (?,?,?,?,?,?,?,?)"
        self.db.execute(sql, (apt.address, apt.city, apt.total_area, apt.rooms, apt.floor, apt.price, apt.property_type.name, 1 if apt.is_available else 0))
        apt.id = self.db.get_last_id()
        self.db.conn.commit()
        return apt.id

    def get_apartment(self, id):
        row = self.db.fetchone("SELECT * FROM apartments WHERE id=?", (id,))
        if not row:
            return None
        return Apartment(row["id"], row["address"], row["city"], row["total_area"], row["rooms"], row["floor"], row["price"], PropertyType[row["property_type"]], bool(row["is_available"]))

    def get_all_apartments(self):
        rows = self.db.fetchall("SELECT * FROM apartments")
        return [self._row_to_apt(r) for r in rows]

    def update_apartment(self, apt):
        sql = "UPDATE apartments SET address=?,city=?,total_area=?,rooms=?,floor=?,price=?,property_type=?,is_available=? WHERE id=?"
        self.db.execute(sql, (apt.address, apt.city, apt.total_area, apt.rooms, apt.floor, apt.price, apt.property_type.name, 1 if apt.is_available else 0, apt.id))
        self.db.conn.commit()

    def delete_apartment(self, id):
        self.db.execute("DELETE FROM apartments WHERE id=?", (id,))
        self.db.conn.commit()

    def find_apartments_by_city(self, city):
        rows = self.db.fetchall("SELECT * FROM apartments WHERE city LIKE ?", (f"%{city}%",))
        return [self._row_to_apt(r) for r in rows]

    def _row_to_apt(self, row):
        return Apartment(row["id"], row["address"], row["city"], row["total_area"], row["rooms"], row["floor"], row["price"], PropertyType[row["property_type"]], bool(row["is_available"]))

    # ---------- Client ----------
    def add_client(self, cl):
        self.db.execute("INSERT INTO clients (name,phone,email) VALUES (?,?,?)", (cl.name, cl.phone, cl.email))
        cl.id = self.db.get_last_id()
        self.db.conn.commit()
        return cl.id

    def get_client(self, id):
        row = self.db.fetchone("SELECT * FROM clients WHERE id=?", (id,))
        if not row:
            return None
        return Client(row["id"], row["name"], row["phone"], row["email"])

    def get_all_clients(self):
        rows = self.db.fetchall("SELECT * FROM clients")
        return [Client(r["id"], r["name"], r["phone"], r["email"]) for r in rows]

    def update_client(self, cl):
        self.db.execute("UPDATE clients SET name=?,phone=?,email=? WHERE id=?", (cl.name, cl.phone, cl.email, cl.id))
        self.db.conn.commit()

    def delete_client(self, id):
        self.db.execute("DELETE FROM clients WHERE id=?", (id,))
        self.db.conn.commit()

    # ---------- Deal ----------
    def add_deal(self, deal):
        sql = "INSERT INTO deals (apartment_id,client_id,deal_type,deal_status,amount) VALUES (?,?,?,?,?)"
        self.db.execute(sql, (deal.apartment_id, deal.client_id, deal.deal_type.name, deal.deal_status.name, deal.amount))
        deal.id = self.db.get_last_id()
        self.db.conn.commit()
        return deal.id

    def get_deal(self, id):
        row = self.db.fetchone("SELECT * FROM deals WHERE id=?", (id,))
        if not row:
            return None
        return Deal(row["id"], row["apartment_id"], row["client_id"], DealType[row["deal_type"]], DealStatus[row["deal_status"]], row["amount"])

    def get_all_deals(self):
        rows = self.db.fetchall("SELECT * FROM deals")
        return [Deal(r["id"], r["apartment_id"], r["client_id"], DealType[r["deal_type"]], DealStatus[r["deal_status"]], r["amount"]) for r in rows]

    def update_deal(self, deal):
        sql = "UPDATE deals SET apartment_id=?,client_id=?,deal_type=?,deal_status=?,amount=? WHERE id=?"
        self.db.execute(sql, (deal.apartment_id, deal.client_id, deal.deal_type.name, deal.deal_status.name, deal.amount, deal.id))
        self.db.conn.commit()

    def delete_deal(self, id):
        self.db.execute("DELETE FROM deals WHERE id=?", (id,))
        self.db.conn.commit()

    def find_deals_by_status(self, status):
        rows = self.db.fetchall("SELECT * FROM deals WHERE deal_status=?", (status.name,))
        return [Deal(r["id"], r["apartment_id"], r["client_id"], DealType[r["deal_type"]], DealStatus[r["deal_status"]], r["amount"]) for r in rows]