from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "data.db"

# 初始化資料庫
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# 取得所有使用者
@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(users=[{"id": r[0], "name": r[1], "email": r[2]} for r in rows])

# 新增使用者
@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

    return jsonify(message="User added successfully"), 201

# 更新使用者
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, user_id))
    conn.commit()
    conn.close()

    return jsonify(message="User updated successfully")

# 刪除使用者
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify(message="User deleted successfully")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

