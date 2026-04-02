"""
Модуль тестов для системы управления недвижимостью.
Содержит тесты для моделей и менеджера.
"""
import unittest
import os
import sys

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.types import DealType, PropertyType, DealStatus
from database.errors import ValidationError
from models.apartment import Apartment
from models.client import Client
from models.deal import Deal


class TestApartment(unittest.TestCase):
    """Тесты для класса Apartment."""
    
    def setUp(self) -> None:
        """Настройка перед каждым тестом."""
        self.apartment = Apartment(
            address="ул. Тестовая, д. 1",
            city="Москва",
            district="Тестовый",
            total_area=50.0,
            living_area=30.0,
            rooms=2,
            floor=5,
            total_floors=10,
            price=5000000.0,
            property_type=PropertyType.APARTMENT,
            description="Тестовая квартира"
        )
    
    def test_apartment_creation(self) -> None:
        """Тест создания квартиры."""
        self.assertEqual(self.apartment.address, "ул. Тестовая, д. 1")
        self.assertEqual(self.apartment.city, "Москва")
        self.assertEqual(self.apartment.total_area, 50.0)
        self.assertEqual(self.apartment.rooms, 2)
    
    def test_apartment_validate(self) -> None:
        """Тест валидации квартиры."""
        self.assertTrue(self.apartment.validate())
    
    def test_apartment_get_info(self) -> None:
        """Тест получения информации о квартире."""
        info = self.apartment.get_info()
        self.assertIn("Двухкомнатная квартира", info)
        self.assertIn("Москва", info)
        self.assertIn("50.0 м²", info)
    
    def test_calculate_price_per_sqm(self) -> None:
        """Тест расчета стоимости за квадратный метр."""
        price_per_sqm = self.apartment.calculate_price_per_sqm()
        self.assertEqual(price_per_sqm, 100000.0)
    
    def test_invalid_total_area(self) -> None:
        """Тест с некорректной площадью."""
        with self.assertRaises(ValidationError):
            self.apartment.total_area = -10
    
    def test_floor_greater_than_total_floors(self) -> None:
        """Тест с этажом больше общего количества этажей."""
        apartment = Apartment(
            address="ул. Тестовая, д. 1",
            city="Москва",
            total_area=50.0,
            rooms=2,
            floor=15,
            total_floors=10,
            price=5000000.0
        )
        self.assertFalse(apartment.validate())


class TestClient(unittest.TestCase):
    """Тесты для класса Client."""
    
    def setUp(self) -> None:
        """Настройка перед каждым тестом."""
        self.client = Client(
            full_name="Иванов Иван Иванович",
            phone="+7(900)123-45-67",
            email="ivanov@example.com",
            passport_series="4500",
            passport_number="123456"
        )
    
    def test_client_creation(self) -> None:
        """Тест создания клиента."""
        self.assertEqual(self.client.full_name, "Иванов Иван Иванович")
        self.assertEqual(self.client.phone, "+7(900)123-45-67")
    
    def test_client_validate(self) -> None:
        """Тест валидации клиента."""
        self.assertTrue(self.client.validate())
    
    def test_client_get_info(self) -> None:
        """Тест получения информации о клиенте."""
        info = self.client.get_info()
        self.assertIn("Иванов Иван Иванович", info)
        self.assertIn("+7(900)123-45-67", info)
    
    def test_add_bonus(self) -> None:
        """Тест начисления бонусов."""
        self.client.add_bonus(100)
        self.assertEqual(self.client.bonus_points, 100)
    
    def test_use_bonus(self) -> None:
        """Тест использования бонусов."""
        self.client.add_bonus(100)
        result = self.client.use_bonus(50)
        self.assertTrue(result)
        self.assertEqual(self.client.bonus_points, 50)
    
    def test_get_client_status(self) -> None:
        """Тест получения статуса клиента."""
        self.assertEqual(self.client.get_client_status(), "Новый")
        self.client.increment_deal_count()
        self.client.increment_deal_count()
        self.assertEqual(self.client.get_client_status(), "Постоянный")
    
    def test_invalid_email(self) -> None:
        """Тест с некорректным email."""
        with self.assertRaises(ValidationError):
            self.client.email = "invalid_email"


class TestDeal(unittest.TestCase):
    """Тесты для класса Deal."""
    
    def setUp(self) -> None:
        """Настройка перед каждым тестом."""
        self.deal = Deal(
            apartment_id=1,
            client_id=1,
            deal_type=DealType.SALE,
            deal_status=DealStatus.DRAFT,
            amount=5000000.0,
            commission_rate=2.0
        )
    
    def test_deal_creation(self) -> None:
        """Тест создания сделки."""
        self.assertEqual(self.deal.amount, 5000000.0)
        self.assertEqual(self.deal.deal_type, DealType.SALE)
    
    def test_deal_validate(self) -> None:
        """Тест валидации сделки."""
        self.assertTrue(self.deal.validate())
    
    def test_deal_get_info(self) -> None:
        """Тест получения информации о сделке."""
        info = self.deal.get_info()
        self.assertIn("Сделка", info)
        self.assertIn("Продажа", info)
    
    def test_calculate_commission(self) -> None:
        """Тест расчета комиссии."""
        commission = self.deal.calculate_commission()
        self.assertEqual(commission, 100000.0)
    
    def test_calculate_net_amount(self) -> None:
        """Тест расчета суммы после комиссии."""
        net_amount = self.deal.calculate_net_amount()
        self.assertEqual(net_amount, 4900000.0)
    
    def test_activate_deal(self) -> None:
        """Тест активации сделки."""
        result = self.deal.activate()
        self.assertTrue(result)
        self.assertEqual(self.deal.deal_status, DealStatus.ACTIVE)
    
    def test_complete_deal(self) -> None:
        """Тест завершения сделки."""
        self.deal.activate()
        result = self.deal.complete()
        self.assertTrue(result)
        self.assertEqual(self.deal.deal_status, DealStatus.COMPLETED)
    
    def test_cancel_deal(self) -> None:
        """Тест отмены сделки."""
        result = self.deal.cancel()
        self.assertTrue(result)
        self.assertEqual(self.deal.deal_status, DealStatus.CANCELLED)


class TestRealEstateManager(unittest.TestCase):
    """Тесты для класса RealEstateManager."""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Настройка перед всеми тестами."""
        cls.test_db_path = "test_real_estate.db"
        
        # Импортируем менеджер после настройки пути
        from manager.real_estate_manager import RealEstateManager
        
        cls.manager = RealEstateManager(cls.test_db_path)
        
        # Инициализируем схему БД
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "database",
            "schema.sql"
        )
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        cls.manager.init_database(schema_sql)
    
    @classmethod
    def tearDownClass(cls) -> None:
        """Очистка после всех тестов."""
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
    
    def test_add_and_get_apartment(self) -> None:
        """Тест добавления и получения квартиры."""
        apartment = Apartment(
            address="ул. Тестовая, д. 100",
            city="Москва",
            district="Тестовый",
            total_area=60.0,
            rooms=2,
            floor=5,
            total_floors=10,
            price=7000000.0,
            property_type=PropertyType.APARTMENT
        )
        
        apt_id = self.manager.add_apartment(apartment)
        self.assertGreater(apt_id, 0)
        
        retrieved = self.manager.get_apartment_by_id(apt_id)
        self.assertEqual(retrieved.address, apartment.address)
        self.assertEqual(retrieved.price, apartment.price)
    
    def test_add_and_get_client(self) -> None:
        """Тест добавления и получения клиента."""
        client = Client(
            full_name="Тестовый Тест Тестович",
            phone="+7(999)000-00-00",
            email="test@example.com"
        )
        
        client_id = self.manager.add_client(client)
        self.assertGreater(client_id, 0)
        
        retrieved = self.manager.get_client_by_id(client_id)
        self.assertEqual(retrieved.full_name, client.full_name)
    
    def test_add_and_get_deal(self) -> None:
        """Тест добавления и получения сделки."""
        # Сначала создаем квартиру и клиента
        apartment = Apartment(
            address="ул. Сделочная, д. 1",
            city="Москва",
            total_area=40.0,
            rooms=1,
            floor=3,
            total_floors=5,
            price=4000000.0
        )
        apt_id = self.manager.add_apartment(apartment)
        
        client = Client(
            full_name="Покупатель Покупатель Покупателевич",
            phone="+7(888)111-22-33"
        )
        client_id = self.manager.add_client(client)
        
        deal = Deal(
            apartment_id=apt_id,
            client_id=client_id,
            deal_type=DealType.SALE,
            amount=4000000.0,
            commission_rate=2.5
        )
        
        deal_id = self.manager.add_deal(deal)
        self.assertGreater(deal_id, 0)
        
        retrieved = self.manager.get_deal_by_id(deal_id)
        self.assertEqual(retrieved.amount, deal.amount)
    
    def test_find_apartments_by_criteria(self) -> None:
        """Тест поиска квартир по критериям."""
        results = self.manager.find_apartments_by_criteria(
            city="Москва",
            min_price=1000000,
            max_price=10000000
        )
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_update_apartment(self) -> None:
        """Тест обновления квартиры."""
        apartment = Apartment(
            address="ул. Обновляемая, д. 5",
            city="Москва",
            total_area=55.0,
            rooms=2,
            floor=4,
            total_floors=9,
            price=6500000.0
        )
        
        apt_id = self.manager.add_apartment(apartment)
        apartment.id = apt_id
        apartment.price = 6000000.0
        
        result = self.manager.update_apartment(apartment)
        self.assertTrue(result)
        
        updated = self.manager.get_apartment_by_id(apt_id)
        self.assertEqual(updated.price, 6000000.0)
    
    def test_delete_apartment(self) -> None:
        """Тест удаления квартиры."""
        apartment = Apartment(
            address="ул. Удаляемая, д. 999",
            city="Москва",
            total_area=30.0,
            rooms=1,
            floor=1,
            total_floors=5,
            price=3000000.0
        )
        
        apt_id = self.manager.add_apartment(apartment)
        result = self.manager.delete_apartment(apt_id)
        self.assertTrue(result)
        
        with self.assertRaises(Exception):
            self.manager.get_apartment_by_id(apt_id)


if __name__ == "__main__":
    unittest.main(verbosity=2)
