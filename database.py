import sqlite3
import hashlib

DB_PATH = "jarvis.db"

def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, u TEXT UNIQUE, p TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS msgs (uid INTEGER, role TEXT, content TEXT)')
    conn.commit()
    conn.close()

def create_user(u, p):
    hp = hashlib.sha256(p.encode()).hexdigest()
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO users (u, p) VALUES (?, ?)", (u, hp))
        conn.commit()
        return True
    except: return False
    finally: conn.close()

def verify_user(u, p):
    hp = hashlib.sha256(p.encode()).hexdigest()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    user = conn.execute("SELECT * FROM users WHERE u = ? AND p = ?", (u, hp)).fetchone()
    conn.close()
    return user

def add_msg(uid, role, content):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO msgs (uid, role, content) VALUES (?, ?, ?)", (uid, role, content))
    conn.commit()
    conn.close()

def get_hist(uid):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    res = conn.execute("SELECT role, content FROM msgs WHERE uid = ? ORDER BY rowid DESC LIMIT 15", (uid,)).fetchall()
    conn.close()
    return res
