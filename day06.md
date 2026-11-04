# День 6 — База данных (PostgreSQL)

### Контейнер db
- IP: 10.191.30.119
- PostgreSQL 14
- База: qa_polygon
- Пользователь: qa_user / qa_password

### Таблица users
- id SERIAL PRIMARY KEY
- email VARCHAR(255) UNIQUE NOT NULL
- password VARCHAR(255) NOT NULL
- name VARCHAR(255)

### Данные
- user@example.com / Password123 / Test User
- admin@example.com / Admin123 / Admin

### Проверка
- psql -h 10.191.30.119 -U qa_user -d qa_polygon → подключение работает
- SELECT * FROM users → две строки

### Что дальше
- Подключить API к БД (заменить JSON на PostgreSQL)

### Подключение API к PostgreSQL

### Права в PostgreSQL
- GRANT ALL PRIVILEGES ON DATABASE — только на подключение к базе
- На таблицы нужно выдавать отдельно: GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE users TO qa_user
- На sequence (для SERIAL) отдельно: GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO qa_user
- Права по умолчанию: ALTER DEFAULT PRIVILEGES

### Контейнер db
- IP: 10.191.30.119
- База: qa_polygon
- Пользователь: qa_user / qa_password
- Таблица: users (id, email, password, name)

### API (Flask)
- Файл /opt/api/server.py
- Использует psycopg2 для подключения к БД
- SELECT для чтения пользователей
- INSERT для создания
- Параметризованные запросы (защита от SQL-инъекций)

### Проверка
- curl http://10.191.30.183:3000/users → JSON с пользователями
- curl http://10.191.30.68/api/users → JSON через прокси
- Форма логина работает: верные данные → welcome.html, неверные → ошибка

### SQL
- CREATE DATABASE qa_polygon
- CREATE USER qa_user WITH PASSWORD 'qa_password'
- GRANT ALL PRIVILEGES ON DATABASE qa_polygon TO qa_user
- GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE users TO qa_user
- GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO qa_user
- SELECT * FROM users
- INSERT INTO users (email, password, name) VALUES (...)


Проверка БД — часть тестирования: данные должны сохраняться

- SQL — базовый навык: SELECT, INSERT, UPDATE, DELETE

- Подключение к БД — QA часто проверяет данные напрямую
