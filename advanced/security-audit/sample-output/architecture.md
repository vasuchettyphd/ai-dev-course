# Architecture summary - leaky-notes (quick profile, partial pass)

**Product and principals.** A ~100-line Flask 3.1.3 JSON API (`app.py`) for per-user notes and invoices, backed by SQLite (`notes.db`) with `uploads/` and `avatars/` directories. `app.py:3-4` states it is deliberately vulnerable and loopback-only. Principals: anonymous client (`POST /login`, `GET /avatars/<path>`) and authenticated user (alice id 1, bob id 2 per `seed.py:16`). There is no admin role. Protected resources: other users' notes and invoices, the `users` table (plaintext passwords, `seed.py:13`), files readable by the server process, and session identity.

**Comparable software.** None is source-grounded (no docs or vendored code).

**Stack and deployment.** Python, Flask dev server via `python app.py`, bound to 127.0.0.1 (`app.py:100-101`). No tests, CI, Dockerfile, proxy, or WSGI config. `notes.db`, `uploads/`, `avatars/` exist only after `seed.py`. Offline execution would need a verified sandbox and already-installed Flask; neither could be verified in this run (see run-metadata), so no target code was executed.

**Entry surfaces and paths.**
- `POST /login` (`app.py:43-53`): `get_json(force=True)`, parameterized lookup, plaintext password compare, writes `session["user_id"]`, no session reset.
- `GET /notes?sort=` (`app.py:56-64`): `sort` goes through the `SORT_COLUMNS` allowlist (`app.py:19`), then an f-string into `ORDER BY`; owner bound by parameter.
- `GET /notes/search?q=` (`app.py:67-73`): `q` and `user_id` interpolated into SQL (`app.py:71`); rows returned as JSON.
- `GET /invoices/<int:id>` (`app.py:76-85`): requires login but never compares `owner_id` to the session user.
- `GET /attachments?name=` (`app.py:88-92`): `os.path.join(UPLOAD_DIR, name)` into `send_file`, no containment.
- `GET /avatars/<path>` (`app.py:95-97`): `send_from_directory` (contained), no login required.
- Session cookie: Flask signed cookie, secret hard-coded at `app.py:17`; `current_user()` (`app.py:36-40`) is the only auth gate.

**Trust boundaries and strongest source-visible control.**
- Anonymous → authenticated: `current_user()` signature check on a cookie whose key is public in source.
- User → other users' data: `owner_id = ?` in `/notes` only; missing or bypassable elsewhere.
- User → filesystem: none on `/attachments`; `safe_join` on `/avatars`.

**Starting paths.** `app.py`, `seed.py`, `requirements.txt`.

**Prior coverage.** No prior runs; no compatible ledgers. No same-source exclusions.

**Companion selection.** `WEB-PROTOCOL-AND-AUTH.md` (cookie sessions, auth gate, CSRF/session blocks). Excluded: `DATA-ISOLATION-AND-LIFECYCLE.md` (no cache, search index, export, deletion, or restore lifecycle; owner scoping is covered by the Access control class); all other companions (no client-side code, protocols, cloud config, native code, LLM, release tooling, or availability surface).
