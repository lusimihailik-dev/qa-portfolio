# День 5 — Веб-тестирование: HTTP и DevTools

## Тестовый полигон — Этап 1: nginx

- Контейнер webserver запущен
- IP: 10.191.30.68
- nginx 1.24.0 установлен и работает
- Проверка: curl -I http://10.191.30.68 → 200 OK
- Заголовки: Server: nginx/1.24.0, Content-Type: text/html
- В браузере: http://10.191.30.68 → Welcome to nginx
- Что дальше: заменить страницу на свой тестовый сайт

## Тестовый сайт в полигоне

- Сайт лежит в /var/www/qa-site
- Страницы: index.html, login.html, register.html
- CSS: style.css
- nginx настроен на /var/www/qa-site
- URL: http://10.191.30.68
- Страницы:
  - / — главная
  - /login.html — вход
  - /register.html — регистрация

## Тестовый полигон

### Контейнер webserver
- IP: 10.191.30.68
- nginx 1.24.0
- Сайт: /var/www/qa-site/
- Страницы: index.html, login.html, register.html
- CSS: style.css

### Проверка
- curl http://10.191.30.68 → HTML нашего сайта
- Браузер → главная и логин открылись

### Что можно тестировать
- Формы логина и регистрации
- Валидацию полей
- Навигацию
- Вёрстку
- HTTP-статусы

## Тестовый полигон — конфиг nginx

### Отдельный конфиг
- /etc/nginx/sites-available/qa-polygon
- Симлинк в /etc/nginx/sites-enabled/qa-polygon
- Дефолтный сайт отключён (rm /etc/nginx/sites-enabled/default)

### Содержимое qa-polygon
- listen 80 default_server
- root /var/www/qa-site
- location /api/ → proxy_pass http://10.191.30.183:3000/

### Проверка
- nginx -t → syntax is ok
- nginx -s reload
- curl http://10.191.30.68/ → 200 OK
- curl http://10.191.30.68/api/users → JSON с пользователями

## Тестирование формы логина

### Найденные баги
- BUG-01: 405 при POST на статику (исправлено: GET + fetch)
- BUG-02: 404 после входа — не было welcome.html (исправлено: создали)

### Итог
- Верные данные: user@example.com / Password123 → «Вход выполнен!» → welcome.html
- Неверные данные: wrong@example.com / wrong → «Неверный email или пароль»
- Форма работает

## Тестовый полигон — итог

### Компоненты
- webserver (10.191.30.68): nginx + сайт /var/www/qa-site
- api (10.191.30.183): Flask + /opt/api/server.py
- Конфиг nginx: /etc/nginx/sites-available/qa-polygon

### Страницы
- index.html — главная
- login.html — вход (проверяет через API)
- register.html — регистрация
- welcome.html — после входа

### Тестирование формы логина
- Верные данные: user@example.com / Password123 → «Вход выполнен!» → welcome.html
- Неверные данные: wrong@example.com / wrong → «Неверный email или пароль»

### Найденные баги
- BUG-01: 405 при POST на статику (исправлено: GET + fetch)
- BUG-02: 404 после входа — не было welcome.html (исправлено: создали)
