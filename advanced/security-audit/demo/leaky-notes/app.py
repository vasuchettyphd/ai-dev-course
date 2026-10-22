"""Leaky Notes - a tiny invoice-and-notes app with planted security bugs.

DO NOT DEPLOY. This app is deliberately vulnerable. It exists only so the
security-audit skill has something to find. Run it on 127.0.0.1 only.
"""
import os
import sqlite3

from flask import Flask, abort, g, jsonify, request, send_file, send_from_directory, session

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "notes.db")
UPLOAD_DIR = os.path.join(BASE, "uploads")
AVATAR_DIR = os.path.join(BASE, "avatars")

app = Flask(__name__)
app.secret_key = "leaky-notes-dev-key-2026"

SORT_COLUMNS = {"newest": "created_at DESC", "oldest": "created_at ASC", "title": "title ASC"}


def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def current_user():
    user_id = session.get("user_id")
    if user_id is None:
        abort(401)
    return user_id


@app.post("/login")
def login():
    data = request.get_json(force=True)
    row = db().execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (data.get("username"), data.get("password")),
    ).fetchone()
    if row is None:
        abort(401)
    session["user_id"] = row["id"]
    return jsonify(ok=True)


@app.get("/notes")
def list_notes():
    user_id = current_user()
    order = SORT_COLUMNS.get(request.args.get("sort", "newest"), "created_at DESC")
    rows = db().execute(
        f"SELECT id, title, created_at FROM notes WHERE owner_id = ? ORDER BY {order}",
        (user_id,),
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/notes/search")
def search_notes():
    user_id = current_user()
    q = request.args.get("q", "")
    sql = f"SELECT id, title FROM notes WHERE owner_id = {user_id} AND title LIKE '%{q}%'"
    rows = db().execute(sql).fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/invoices/<int:invoice_id>")
def get_invoice(invoice_id):
    current_user()
    row = db().execute(
        "SELECT id, owner_id, customer, amount_cents FROM invoices WHERE id = ?",
        (invoice_id,),
    ).fetchone()
    if row is None:
        abort(404)
    return jsonify(dict(row))


@app.get("/attachments")
def download_attachment():
    current_user()
    name = request.args.get("name", "")
    return send_file(os.path.join(UPLOAD_DIR, name))


@app.get("/avatars/<path:filename>")
def avatar(filename):
    return send_from_directory(AVATAR_DIR, filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5807")))
