import sqlite3
import random
from faker import Faker

DB_NAME = "hw02.sqlite"
fake = Faker()

def seed_status(cur):
    for name in ("new", "in progress", "completed"):
        cur.execute("INSERT OR IGNORE INTO status (name) VALUES (?)", (name,))

def seed_users(cur, n=10):
    fake.unique.clear()
    for _ in range(n):
        cur.execute(
            "INSERT INTO users (fullname, email) VALUES (?, ?)",
            (fake.name(), fake.unique.email())
        )

def seed_tasks(cur, n=30):
    user_ids  = [r[0] for r in cur.execute("SELECT id FROM users")]
    status_ids = [r[0] for r in cur.execute("SELECT id FROM status")]
    if not user_ids or not status_ids:
        return
    for _ in range(n):
        cur.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
            (fake.sentence(nb_words=4), fake.text(max_nb_chars=100),
             random.choice(status_ids), random.choice(user_ids))
        )

def main():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cur = conn.cursor()
        seed_status(cur)
        seed_users(cur, 10)
        seed_tasks(cur, 30)
        conn.commit()

if __name__ == "__main__":
    main()
