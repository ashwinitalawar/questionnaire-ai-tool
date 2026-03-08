import sqlite3
from passlib.hash import bcrypt

DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def hash_password(password):
    return bcrypt.hash(password)


def register(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "INSERT INTO users (email, password) VALUES (?, ?)",
        (email, hashed_password)
    )

    conn.commit()
    conn.close()


def login(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE email=?",
        (email,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        stored_password = result[0]
        return bcrypt.verify(password, stored_password)

    return False