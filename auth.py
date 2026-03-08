import sqlite3
import hashlib

DB_NAME = "users.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register(email, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hashed_password)
        )
        conn.commit()

    except sqlite3.IntegrityError:
        pass

    conn.close()


def login(email, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, hashed_password)
    )

    result = cursor.fetchone()
    conn.close()

    return result is not None


create_table()