# День 10 — Git → GitHub: портфолио в интернете
## 1. Зачем QA GitHub
- Портфолио — рекрутеры видят твои конспекты, тест-кейсы, баг-репорты.
- Резюме — ссылка на GitHub обязательна для Junior QA.
- Работа в команде — в реальных проектах код и тесты лежат в GitHub.

## 2. Настройка Git
bash
- git config --global user.name lusimihailik-dev
- git config --global user.email lusimihailik@gmail.com
- git config --list

## 3. Создание SSH-ключа
### Зачем: чтобы GitHub узнавал тебя без пароля.

bash
- ssh-keygen -t ed25519 -C lusimihailik@gmail.com

### Что произойдёт:
- Нажми Enter (сохранить в папку по умолчанию).
- Нажми Enter (без пароля) или введи пароль.

### Проверь:

bash
- ls -la ~/.ssh/

Ожидаем: файлы id_ed25519 (приватный) и id_ed25519.pub (публичный).

## 4. Добавление ключа в SSH-агент
bash
- eval "$(ssh-agent -s)"
- ssh-add ~/.ssh/id_ed25519

## 5. Копирование публичного ключа
bash
- cat ~/.ssh/id_ed25519.pub
- Скопируй весь вывод (начинается с ssh-ed25519 ...).

## 6. Добавление ключа на GitHub
- Открой GitHub → Settings.
- Слева: SSH and GPG keys.
- Нажми New SSH key.
- Title: Mila Ubuntu.
- Key: вставь скопированный ключ.
- Нажми Add SSH key.

## 7. Проверка подключения
bash
- ssh -T git@github.com

Ожидаем:

(text)

- Hi username! You've successfully authenticated...

## 8. Создание репозитория на GitHub
- Открой GitHub → New repository.
- Repository name: qa-portfolio
- Visibility: Public.
- НЕ ставь галочку «Initialize with README».
- Нажми Create repository.
- Скопируй URL (SSH): git@github.com:lusimihailik-dev/qa-portfolio.git.

## 9. Инициализация репозитория на хосте
bash
- cd ~/qa-notes
- git init
- git add .
- git commit -m "Initial commit: конспекты и тест-кейсы QA"

## 10. Привязка к GitHub и отправка
bash
- git remote add origin git@github.com:lusimihailik-dev/qa-portfolio.git
- git branch -M main
- git push -u origin main

### Разбор:
- git remote add origin ... — связывает локальный репозиторий с GitHub.
- git branch -M main — переименовывает ветку в main.
- git push -u origin main — отправляет файлы на GitHub.

## 11. Проверка на GitHub
- Открой https://github.com/lusimihailik-dev/qa-portfolio.
- Обнови страницу — должны увидеть все файлы.
- Если файлы на месте — поздравляю, у тебя есть портфолио на GitHub!

## 12. Что внутри портфолио (итог)
Файл / Что внутри
- day01.md … day11.md / 11 конспектов
- test-cases-login.md / 11 тест-кейсов
- bug-report-*.md / 7 баг-репортов
- test-design-*.md / 3 файла тест-дизайна
- README.md / Описание портфолио

- Ссылка на портфолио: https://github.com/lusimihailik-dev/qa-portfolio
