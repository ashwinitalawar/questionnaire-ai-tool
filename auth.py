import sqlite3
import hashlib

# connect to database
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
email TEXT UNIQUE,
password TEXT
)
""")

conn.commit()


# hash password using SHA256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register(email, password):

    hashed_password = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users(email, password) VALUES (?, ?)",
            (email, hashed_password)
        )
        conn.commit()
    except:
        pass


def login(email, password):

    hashed_password = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, hashed_password)
    )

    user = cursor.fetchone()

    if user:
        return True

    return False