from flask import Flask, request, jsonify
import psycopg2
import bcrypt
import jwt
import datetime
import re
from functools import wraps

app = Flask(__name__)

DB_CONFIG = {
    "host": "10.191.30.51",
    "port": 5432,
    "database": "qa_polygon",
    "user": "qa_user",
    "password": "qa_password"
}

SECRET_KEY = "qa-polygon-secret-key-2026"  # в реальности — из переменной окружения

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Токен отсутствует"}), 401
        try:
            token = token.split(" ")[1]  # Bearer <token>
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return jsonify({"message": "Неверный токен"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/users/me', methods=['GET'])
@token_required
def get_current_user():
    token = request.headers.get('Authorization').split(" ")[1]
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = data.get('id')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, name FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"message": "Пользователь не найден"}), 404

    return jsonify({"id": row[0], "email": row[1], "name": row[2]})

@app.route('/change-password', methods=['POST'])
@token_required
def change_password():
    token = request.headers.get('Authorization').split(" ")[1]
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = data.get('id')

    body = request.get_json()
    old_password = body.get('old_password')
    new_password = body.get('new_password')

    if not old_password or not new_password:
        return jsonify({"message": "Все поля обязательны"}), 400

    if len(new_password) < 8:
        return jsonify({"message": "Пароль должен быть не менее 8 символов"}), 400

    if '<' in new_password or '>' in new_password:
        return jsonify({"message": "Пароль содержит недопустимые символы"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()

    if not row:
        return jsonify({"message": "Пользователь не найден"}), 404

    if not bcrypt.checkpw(old_password.encode('utf-8'), row[0].encode('utf-8')):
        return jsonify({"message": "Неверный старый пароль"}), 401

    new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cur.execute("UPDATE users SET password = %s WHERE id = %s", (new_hash, user_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Пароль успешно изменён"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, password, name FROM users WHERE email = %s", (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"message": "Неверный email или пароль"}), 401

    if not bcrypt.checkpw(password.encode('utf-8'), row[2].encode('utf-8')):
        return jsonify({"message": "Неверный email или пароль"}), 401

    token = jwt.encode({
        "id": row[0],
        "email": row[1],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token, "user": {"id": row[0], "email": row[1], "name": row[3]}})

@app.route('/users', methods=['GET'])
@token_required
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, name FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "email": r[1], "name": r[2]} for r in rows])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    password = data.get('password')
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, password, name) VALUES (%s, %s, %s) RETURNING id",
        (data.get('email'), password_hash.decode('utf-8'), data.get('name', ''))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "email": data.get('email'), "name": data.get('name', '')}), 201

@app.route('/tasks', methods=['GET'])
@token_required
def get_tasks():
    token = request.headers.get('Authorization').split(" ")[1]
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = data.get('id')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, status, created_at FROM tasks WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {"id": r[0], "title": r[1], "status": r[2], "created_at": r[3].isoformat()}
        for r in rows
    ])

@app.route('/tasks', methods=['POST'])
@token_required
def create_task():
    token = request.headers.get('Authorization').split(" ")[1]
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = data.get('id')

    body = request.get_json()
    title = body.get('title')

    if not title or len(title.strip()) == 0:
        return jsonify({"message": "Название задачи обязательно"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (user_id, title) VALUES (%s, %s) RETURNING id, title, status, created_at",
        (user_id, title)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id": row[0],
        "title": row[1],
        "status": row[2],
        "created_at": row[3].isoformat()
    }), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):
    token = request.headers.get('Authorization').split(" ")[1]
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = data.get('id')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s RETURNING id", (task_id, user_id))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"message": "Задача не найдена"}), 404

    return jsonify({"message": "Задача удалена"})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    token = request.headers.get('Authorization').split(" ")[1]
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = data.get('id')

    body = request.get_json()
    title = body.get('title')
    status = body.get('status')

    if not title and not status:
        return jsonify({"message": "Нужно передать title или status"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Проверяем, что задача принадлежит пользователю
    cur.execute("SELECT id FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"message": "Задача не найдена"}), 404

    if title:
        cur.execute("UPDATE tasks SET title = %s WHERE id = %s", (title, task_id))
    if status:
        if status not in ('new', 'in_progress', 'done'):
            cur.close()
            conn.close()
            return jsonify({"message": "Недопустимый статус"}), 400
        cur.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, task_id))

    conn.commit()

    cur.execute("SELECT id, title, status, created_at FROM tasks WHERE id = %s", (task_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    return jsonify({
        "id": row[0],
        "title": row[1],
        "status": row[2],
        "created_at": row[3].isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
