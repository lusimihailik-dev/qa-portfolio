# День 11 — JWT-авторизация и фиксация IP

## 1. Что такое JWT и зачем он нужен

JWT (JSON Web Token) — способ передать информацию о пользователе в виде подписанного токена.

Проблема, которую решает JWT: раньше API отдавал данные без проверки (BUG-04: список пользователей без авторизации). JWT решает это: сервер выдаёт токен после логина и требует его для защищённых эндпоинтов.

Как работает:
1. Пользователь логинится (email + пароль) → POST /login
2. Сервер проверяет пароль и выдаёт токен
3. Клиент сохраняет токен в localStorage
4. При каждом запросе клиент отправляет токен в заголовке Authorization: Bearer <токен>
5. Сервер проверяет подпись и пускает пользователя

Состав JWT: header.payload.signature
- header — алгоритм (HS256)
- payload — данные (id, email, exp)
- signature — подпись от подделки

## 2. Что даёт токен

- Доступ к защищённым эндпоинтам (/users)
- Сервер не хранит сессии (stateless)
- Срок действия 1 час (exp)
- Передаётся в заголовке Authorization (не в URL)

Что токен не даёт:
- Не даёт доступ к чужим данным (если сервер проверяет id)
- Не защищает от кражи токена

## 3. Установка PyJWT

lxc exec api bash
pip3 install PyJWT
python3 -c "import jwt; print('OK')"

## 4. Основные эндпоинты

### /login (POST)
Принимает email и password. Проверяет через bcrypt.checkpw.
Возвращает токен и данные пользователя.

### /users (GET) — защищённый
Требует заголовок Authorization: Bearer <токен>.
Без токена → 401 Unauthorized.

## 5. Как получить и использовать токен

Получить токен:
curl -X POST http://10.191.30.50:3000/login -H "Content-Type: application/json" -d '{"email":"user@example.com","password":"Password123"}'

Использовать токен:
curl http://10.191.30.50:3000/users -H "Authorization: Bearer <токен>"

## 6. Проверка JWT (что проверяет QA)

- Без токена → 401
- С валидным токеном → 200
- С поддельным токеном → 401 (подпись не совпала)
- С просроченным токеном → 401 (срок истёк)
- С токеном другого пользователя → проверить IDOR

## 7. Что лежит внутри токена

Payload:
{
  "id": 1,
  "email": "user@example.com",
  "exp": 1700000000
}

Чего там быть не должно:
- Пароля
- Секретных данных

## 8. Фиксация IP-адресов контейнеров

Проблема: LXD выдаёт IP динамически, при перезапуске IP может измениться. Это ломает nginx и подключение к БД.

Решение:
1. Сузить пул DHCP:
   lxc network set lxdbr0 ipv4.dhcp.ranges 10.191.30.100-10.191.30.150

2. Назначить статические IP (вне пула):
   lxc config device override api eth0 ipv4.address=10.191.30.50
   lxc config device override db eth0 ipv4.address=10.191.30.51
   lxc config device override webserver eth0 ipv4.address=10.191.30.52
   lxc config device override redmine eth0 ipv4.address=10.191.30.53
   lxc config device override qa-base eth0 ipv4.address=10.191.30.54

3. Перезапустить контейнеры:
   lxc restart api && lxc restart db && lxc restart webserver && lxc restart redmine && lxc restart qa-base

4. Проверить:
   lxc list

Итоговая таблица IP:
- api — 10.191.30.50
- db — 10.191.30.51
- webserver — 10.191.30.52
- redmine — 10.191.30.53
- qa-base — 10.191.30.54

После смены IP обновить:
- nginx в webserver: proxy_pass http://10.191.30.50:3000/
- server.py в api: "host": "10.191.30.51"

## 9. Найденные баги

BUG-04 — частично исправлен:
- Раньше /users был доступен без токена
- Теперь только с токеном (401 без токена)
- Логин через POST (не GET, пароль не в URL)

BUG-07 — новый:
- /users возвращает всех пользователей любому авторизованному
- Severity: High (утечка PII)
- Priority: High
- Рекомендация: ограничить /users только админу, добавить /users/me

## 10. Автозапуск (systemd)

Redmine (/etc/systemd/system/redmine.service):
[Unit]
Description=Redmine (Puma)
After=network.target postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/redmine-src
Environment=RAILS_ENV=production
ExecStart=/usr/local/bin/bundle exec rails server -e production -b 0.0.0.0 -p 3000
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

API (/etc/systemd/system/qa-api.service):
[Unit]
Description=QA Polygon Flask API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/api
ExecStart=/usr/bin/python3 /opt/api/server.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

Включить и запустить:
systemctl daemon-reload
systemctl enable redmine qa-api
systemctl start redmine qa-api

Проверка:
systemctl status redmine --no-pager
systemctl status qa-api --no-pager

## 11. Итог Дня 11

- Установлен PyJWT
- /login выдаёт токен
- /users требует токен
- Форма логина сохраняет токен в localStorage
- Проверены сценарии: без токена, с токеном, поддельный, просроченный
- IP-адреса зафиксированы
- Найден BUG-07
- Настроен автозапуск (systemd)

## Что было непонятно
- ...
