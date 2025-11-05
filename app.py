import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = ":memory:"  # 使用 in-memory DB
conn = None  # 全域連線

def init_db():
    global conn
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)  # 允許多線程使用同一連線
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()

# GET /users
@app.route("/users", methods=["GET"])
def get_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return jsonify(users=[{"id": r[0], "name": r[1], "email": r[2]} for r in rows])

# POST /users
@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    return jsonify(message="User added successfully"), 201

# PUT /users/<id>
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, user_id))
    conn.commit()
    return jsonify(message="User updated successfully")

# DELETE /users/<id>
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    return jsonify(message="User deleted successfully")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, threaded=True)
