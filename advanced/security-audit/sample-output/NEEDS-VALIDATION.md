# Needs validation (run-1)

Four leads, no severity assigned, none a confirmed vulnerability. In each case the source trace was independently re-read by a fresh verifier. The only decisive missing item is a bounded local observed result, because no OS-enforced sandbox could be verified on the host. Machine-readable copies are in `findings.json`. All local plans use a scratch copy of the repo, a freshly seeded dummy `notes.db`, the already-installed Flask, `python -I`, and `app.test_client()` with no network.

Priority order is by resource protected, then by how much of the trace is in source alone.

## 1. `app.py:download_attachment:send-file-path-traversal`: arbitrary file read via `/attachments`

- **Boundary:** user to server filesystem. The lower-trust principal is any logged-in user.
- **Trace:** `app.py:88` entrypoint (`current_user()` at `90` checks only that a session exists) → `91` `name` read from the query string unvalidated → `92` `os.path.join(UPLOAD_DIR, name)` (absolute `name` discards `UPLOAD_DIR`, `../` escapes) → `92` `send_file(...)` sink.
- **Evidence:** no containment before `send_file`; `/avatars` uses `send_from_directory` (`app.py:97`) as a contrast; `notes.db` with plaintext passwords (`seed.py:13`) is one `../` away. A verifier read Flask 3.1.3 `helpers.send_file` and Werkzeug 3.1.9 `utils.send_file` in a local uv cache and found no `safe_join` on this path.
- **Blockers:** no verified sandbox; library behavior was read, not observed; whether that cached version is what runs the app is not established; filesystem permissions and any front-end that normalizes paths are not visible from source.
- **Local plan:** seed a scratch copy; control `GET /attachments?name=welcome.txt` unauthenticated expects 401, logged in as alice expects 200; test `?name=../notes.db` expects 200 with a body starting `SQLite format 3` if real; also the absolute path of the copy's own `seed.py`; contrast `GET /avatars/..%2Fnotes.db` expects 404. After switching to `send_from_directory`, the two traversal requests must return 404.
- **Owner-observed check:** none needed beyond the local plan.
- **Smallest fix:** `send_from_directory(UPLOAD_DIR, name)`, or `werkzeug.security.safe_join` with `abort(404)` on `None`.

## 2. `app.py:secret_key:hardcoded-session-signing-key`: forgeable session cookie

- **Boundary:** anonymous to authenticated, and user to other users' identity.
- **Trace:** `app.py:17` literal `secret_key` → `37` `session.get('user_id')` trusted once the signature verifies → `58` `list_notes` uses the returned id → `60` notes query with the forged `owner_id`. The same cookie would pass every `current_user()` gate.
- **Evidence:** no key override in source (the only environment read is `PORT`, `app.py:101`); `current_user()` has no server-side session record or user-existence check (`app.py:36-40`); user ids 1 and 2 are known from `seed.py:16`.
- **Blockers:** no verified sandbox; the verifier did not find Flask/itsdangerous source, so cookie acceptance is unverified; exploitation requires knowing the key, so it depends on who can read the repository, which source cannot establish. The docstring (`app.py:3-4`) and loopback bind (`app.py:101`) are context, not mitigations.
- **Local plan:** in a separate script with the installed Flask, `a = Flask('x'); a.secret_key = <literal from app.py:17>; c = a.session_interface.get_signing_serializer(a).dumps({'user_id': 2})`. With `app.test_client()` and no login, send `GET /notes` with that cookie. HTTP 200 containing `Bob secret plans` would confirm it. Control: a cookie signed with a different key must return 401.
- **Owner-observed check:** confirm whether any running instance is configured with the committed key, or rotate the key and confirm old cookies are rejected. No audit traffic should be sent to a deployment.
- **Smallest fix:** read the key from a per-deployment secret (fail startup if absent, at least 32 random bytes) and rotate the committed value.

## 3. `app.py:search_notes:sql-interpolation`: SQL injection in `/notes/search`

- **Boundary:** user to other users' notes and other tables. Lower-trust principal: any logged-in user.
- **Trace:** `app.py:68` entrypoint (`current_user()` at `69`) → `70` `q` read raw → `71` f-string puts `q` inside a quoted `LIKE` literal → `72` `db().execute(sql)` with no parameters; rows returned at `73`.
- **Evidence:** bound parameters are used elsewhere (`app.py:47,61-62,80-81`); the query shape `SELECT id, title` fits a two-column `UNION` against `users` (`seed.py:13`, plaintext passwords). `user_id` comes from the signed session and is not request-controlled here. sqlite3 `execute()` runs one statement, so impact is read access, not stacked writes.
- **Blockers:** no verified sandbox; exact payload behavior (column count, type affinity, comment handling, JSON output) is inferred from SQLite semantics and the seed schema, not observed.
- **Local plan:** log in as alice. Baseline `GET /notes/search?q=Alice` returns only note 1. Scope bypass with `q = zzz%' OR owner_id=2 --` should return `Bob secret plans` if real. `UNION` with `q = zzz%' UNION SELECT id, username||':'||password FROM users --` should return the seeded credentials if real. Repeat after the fix; both must return an empty list. No destructive payloads.
- **Owner-observed check:** none needed.
- **Smallest fix:** `WHERE owner_id = ? AND title LIKE ?` with `(user_id, f"%{q}%")`.

## 4. `app.py:get_invoice:missing-owner-check-idor`: any user can read any invoice

- **Boundary:** user to other users' invoices.
- **Trace:** `app.py:76` entrypoint (`invoice_id` is attacker-chosen) → `78` `current_user()` result discarded → `79` query by `id` only → `85` full row returned including `owner_id`.
- **Evidence:** `list_notes` and `search_notes` assign and use `user_id` while `get_invoice` does not (`app.py:58,69,78`); the SQL has no owner predicate (`app.py:80`); invoice 2 belongs to user 2 (`seed.py:20`). No decorator, hook, or sharing model was found.
- **Blockers:** no verified sandbox. Source review found no refuting control, so this is the lead with the least remaining doubt.
- **Local plan:** log in as alice; `GET /invoices/1` expects 200 with `owner_id` 1; `GET /invoices/2` expects 200 with bob's Globex row if real, or 403/404 if refuted. Control: unauthenticated `GET /invoices/2` expects 401. After the fix, alice requesting invoice 2 must return 404.
- **Owner-observed check:** none needed.
- **Smallest fix:** `user_id = current_user()` and `WHERE id = ? AND owner_id = ?` with 404 on no match.
