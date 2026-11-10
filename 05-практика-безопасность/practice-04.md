# Практика 4 — CORS

## Запрос
curl -I -H "Origin: http://10.191.30.52" -H "Authorization: Bearer <токен>" http://10.191.30.50:3000/users

## Заголовки ответа
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.10.12
Date: Tue, 10 Nov 2026 15:06:01 GMT
Content-Type: application/json
Content-Length: 344
Connection: close

## Вывод
CORS не настроен. Заголовок Access-Control-Allow-Origin отсутствует.
В реальном приложении нужно добавить заголовок, разрешающий запросы
с доверенных доменов.
