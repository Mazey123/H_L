-- DDL схема базы данных для системы "Недвижимость"
-- Тема 21: Недвижимость (квартиры/сделки)

-- Таблица квартир
CREATE TABLE IF NOT EXISTS apartments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    address TEXT NOT NULL,
    area REAL NOT NULL,
    rooms INTEGER NOT NULL,
    price REAL NOT NULL
);

-- Таблица клиентов
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Таблица сделок
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
);

-- DML: Пример данных для демонстрации

-- Добавление квартир
INSERT INTO apartments (title, address, area, rooms, price) VALUES
('Уютная квартира в центре', 'ул. Ленина, 10', 45.5, 2, 5500000),
('Просторная трёшка', 'пр. Мира, 25', 85.0, 3, 8900000),
('Студия возле метро', 'ул. Гагарина, 5', 30.0, 1, 3200000);

-- Добавление клиентов
INSERT INTO clients (title, phone, email) VALUES
('Иван Петров', '+7 999 123-45-67', 'ivan@example.com'),
('Мария Сидорова', '+7 911 987-65-43', 'maria@example.com'),
('Алексей Смирнов', '+7 926 555-12-34', 'alexey@example.com');

-- Добавление сделок
INSERT INTO deals (title, apartment_id, client_id, deal_type, date, amount) VALUES
('Продажа квартиры Ивану', 1, 1, 'sale', '2026-03-12', 5500000),
('Аренда студии', 3, 2, 'rent', '2026-03-15', 35000);
