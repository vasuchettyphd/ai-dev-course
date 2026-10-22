"""Create notes.db with two dummy users. DO NOT DEPLOY - demo data only."""
import os
import sqlite3

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "notes.db")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)
conn.executescript(
    """
    CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT);
    CREATE TABLE notes (id INTEGER PRIMARY KEY, owner_id INTEGER, title TEXT, created_at TEXT);
    CREATE TABLE invoices (id INTEGER PRIMARY KEY, owner_id INTEGER, customer TEXT, amount_cents INTEGER);
    INSERT INTO users VALUES (1, 'alice', 'alice-pw'), (2, 'bob', 'bob-pw');
    INSERT INTO notes VALUES
        (1, 1, 'Alice shopping list', '2026-10-01'),
        (2, 2, 'Bob secret plans', '2026-10-02');
    INSERT INTO invoices VALUES (1, 1, 'Acme Corp', 120000), (2, 2, 'Globex', 990000);
    """
)
conn.commit()
conn.close()
for folder, name, text in (("uploads", "welcome.txt", "Welcome to Leaky Notes.\n"),
                           ("avatars", "default.txt", "(pretend this is a picture)\n")):
    os.makedirs(os.path.join(BASE, folder), exist_ok=True)
    with open(os.path.join(BASE, folder, name), "w") as f:
        f.write(text)
print("Seeded", DB_PATH)
