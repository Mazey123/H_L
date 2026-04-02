-- Схема базы данных для системы управления недвижимостью
-- Тема 21: Недвижимость (квартиры/сделки)

-- Таблица клиентов
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    passport_series TEXT,
    passport_number TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица объектов недвижимости (квартир)
CREATE TABLE IF NOT EXISTS apartments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    district TEXT,
    total_area REAL NOT NULL,
    living_area REAL,
    rooms INTEGER NOT NULL DEFAULT 1,
    floor INTEGER NOT NULL,
    total_floors INTEGER NOT NULL,
    price REAL NOT NULL,
    property_type TEXT NOT NULL DEFAULT 'APARTMENT',
    description TEXT,
    is_available BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица сделок
CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    apartment_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    deal_type TEXT NOT NULL,
    deal_status TEXT NOT NULL DEFAULT 'DRAFT',
    amount REAL NOT NULL,
    commission_rate REAL DEFAULT 2.0,
    deal_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (apartment_id) REFERENCES apartments(id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

-- Индексы для ускорения поиска
CREATE INDEX IF NOT EXISTS idx_apartments_city ON apartments(city);
CREATE INDEX IF NOT EXISTS idx_apartments_price ON apartments(price);
CREATE INDEX IF NOT EXISTS idx_apartments_available ON apartments(is_available);
CREATE INDEX IF NOT EXISTS idx_deals_apartment ON deals(apartment_id);
CREATE INDEX IF NOT EXISTS idx_deals_client ON deals(client_id);
CREATE INDEX IF NOT EXISTS idx_deals_status ON deals(deal_status);

-- Пример данных для тестирования (DML)
INSERT INTO clients (full_name, phone, email, passport_series, passport_number) VALUES
('Иванов Иван Иванович', '+7(900)123-45-67', 'ivanov@example.com', '4500', '123456'),
('Петрова Мария Сергеевна', '+7(900)234-56-78', 'petrova@example.com', '4501', '234567'),
('Сидоров Петр Александрович', '+7(900)345-67-89', 'sidorov@example.com', '4502', '345678');

INSERT INTO apartments (address, city, district, total_area, living_area, rooms, floor, total_floors, price, property_type, description, is_available) VALUES
('ул. Ленина, д. 10, кв. 25', 'Москва', 'Центральный', 65.5, 45.0, 2, 5, 12, 8500000.0, 'APARTMENT', 'Просторная двухкомнатная квартира в центре', 1),
('пр. Мира, д. 45, кв. 102', 'Москва', 'Северный', 42.0, 25.0, 1, 10, 16, 5200000.0, 'STUDIO', 'Светлая студия с панорамными окнами', 1),
('ул. Гагарина, д. 8, кв. 5', 'Москва', 'Южный', 120.0, 90.0, 4, 3, 5, 15000000.0, 'PENTHOUSE', 'Элитный пентхаус с террасой', 1),
('ул. Торговая, д. 15', 'Москва', 'Деловой', 85.0, 70.0, 0, 1, 3, 12000000.0, 'COMMERCIAL', 'Коммерческое помещение на первом этаже', 1);

INSERT INTO deals (apartment_id, client_id, deal_type, deal_status, amount, commission_rate, deal_date, notes) VALUES
(1, 1, 'SALE', 'COMPLETED', 8500000.0, 2.0, '2024-01-15', 'Сделка успешно завершена'),
(2, 2, 'RENT', 'ACTIVE', 50000.0, 5.0, '2024-02-01', 'Аренда на 11 месяцев');
