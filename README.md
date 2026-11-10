# QA Portfolio — Mila

Привет! Я начинающий QA-инженер. Здесь собраны мои конспекты, тест-кейсы, баг-репорты, тест-дизайн, практика по безопасности и код тестового полигона.

## 📁 Структура репозитория

### 01-конспекты
Конспекты по темам (20 дней обучения):
- LXD, Linux, Git, HTTP, PostgreSQL, JWT, Redmine
- Теория QA, тест-дизайн, безопасность API
- Подготовка к собеседованию

### 02-тест-кейсы
- `test-cases-login.md` — 11 тест-кейсов для формы логина (включая SQL-инъекцию и XSS)
- `test-change-password.md` — тесты смены пароля (7 тестов)

### 03-баг-репорты
13 баг-репортов (BUG-01…BUG-13):
- BUG-01: 405 при логине
- BUG-02: 404 после входа
- BUG-03: пароли в открытом виде
- BUG-04: PII + отсутствие авторизации
- BUG-05: логин сломался после хеширования
- BUG-06: 405 при регистрации
- BUG-07: IDOR (все пользователи видны)
- BUG-08: XSS в имени
- BUG-09: нет ссылки на смену пароля
- BUG-10: XSS в пароле
- BUG-11: дубль в навигации
- BUG-12: неконсистентная навигация
- BUG-13: задача не сохраняется без авторизации

### 04-тест-дизайн
- `test-design-age.md` — поле «Возраст»
- `test-design-password.md` — поле «Пароль»
- `test-design-register.md` — форма регистрации

### 05-практика-безопасность
- `practice-01.md` — SQL-инъекция (защищён)
- `practice-02.md` — XSS (уязвимость)
- `practice-03.md` — IDOR (уязвимость)
- `practice-04.md` — CORS (не настроен)

### 06-код-полигона
Код тестового полигона:
- `server.py` — API на Flask + PostgreSQL + JWT
- `profile.html` — личный кабинет
- `change_password.html` — смена пароля
- `tasks.html` — список задач
- `index.html`, `login.html`, `register.html`, `welcome.html` — страницы сайта
- `style.css` — стили

## 🛠 Тестовый полигон

- **5 контейнеров LXD**: qa-base, webserver, api, db, redmine
- **Сайт**: nginx + HTML/CSS/JS
- **API**: Flask + PostgreSQL + JWT + bcrypt
- **БД**: PostgreSQL (таблицы users, tasks)
- **Баг-трекер**: Redmine (13 багов, 9 решены)

## 📄 Резюме
- `resume.md` — резюме Junior QA

## 📬 Контакты
- GitHub: [lusimihailik-dev](https://github.com/lusimihailik-dev)
- Email: oliverludmila@mail.ru
