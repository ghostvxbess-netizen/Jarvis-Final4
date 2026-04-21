import sqlite3
import hashlib
import os
from config import SQLITE_PATH

def get_conn():
    conn = sqlite3.connect(SQLITE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS messages 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def create_user(username, password):
    hash_pw = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn = get_conn()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_pw))
        conn.commit()
        return True
    except:
        return False
    finally: conn.close()

def verify_user(username, password):
    hash_pw = hashlib.sha256(password.encode()).hexdigest()
    conn = get_conn()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_pw)).fetchone()
    conn.close()
    return user

def add_message(user_id, role, content):
    conn = get_conn()
    conn.execute("INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)", (user_id, role, content))
    conn.commit()
    conn.close()

def get_history(user_id, limit=20):
    conn = get_conn()
    rows = conn.execute("SELECT role, content FROM messages WHERE user_id = ? ORDER BY id DESC LIMIT ?", (user_id, limit)).fetchall()
    conn.close()
    return rows

def clear_history(user_id):
    conn = get_conn()
    conn.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
