# Security audit: leaky-notes (run-1)

## Run summary

- **Profile:** `quick`. This is a **partial pass**, not a claim that the rest of the code is clean.
- **Scope:** `app.py`, `seed.py`, `requirements.txt` (the whole repo apart from `.claude/`).
- **Source ref:** commit `d2ee904`, clean worktree.
- **Budget:** 12 agent invocations planned, 11 spent (4 reconnaissance, 2 hunters, 1 final critic, 4 verifiers).
- **Execution:** source-only. No target code was run. A check for bubblewrap and Flask on this host could not be run (the shell required approval), so no OS-enforced sandbox was verified. The skill requires a bounded local observed result before any record can be `confirmed`, so **there are zero confirmed findings and four `needs_validation` leads**.
- **Prior runs:** none. No compatible ledger existed.
- **Process deviations:** hunter and verifier prompts used condensed copies of the method and validation blocks and referenced `report-schema.json` by path. The promotion-procedure block was left out because nothing was executed.

## Security posture

The app is a deliberately vulnerable demo (`app.py:3-4`). Source review found four plausible boundary failures that each map to a documented intentional weakness: a SQL-injectable search, a missing invoice ownership check, an unconstrained file path in `/attachments`, and a hardcoded session-signing key. All four have complete source traces and independent source re-verification. None was reproduced, so none carries a severity.

## Confirmed findings

None. Nothing could be reproduced locally in this run (see Execution above).

## NEEDS VALIDATION

No severity is assigned to these. Each is a source-grounded lead whose only missing piece is a bounded local run. Full traces and plans are in `NEEDS-VALIDATION.md`.

| Lead | Trace | Blocker | Next local step |
|---|---|---|---|
| Path traversal in `GET /attachments` (`app.py:download_attachment:send-file-path-traversal`) | `app.py:88` → `91` → `92` (`os.path.join` into `send_file`) | No verified sandbox; library behavior read from a cache copy, not observed | `app.test_client()` on a seeded scratch copy: `?name=../notes.db` |
| Missing ownership check on `GET /invoices/<id>` (`app.py:get_invoice:missing-owner-check-idor`) | `app.py:76` → `78` → `79` → `85` | No verified sandbox | Log in as alice, `GET /invoices/2`, expect bob's row |
| SQL injection in `GET /notes/search` (`app.py:search_notes:sql-interpolation`) | `app.py:68` → `70` → `71` → `72` | No verified sandbox; payload behavior inferred from SQLite semantics | `q` with `OR owner_id=2` and a `UNION` against `users` |
| Hardcoded session key (`app.py:secret_key:hardcoded-session-signing-key`) | `app.py:17` → `37` → `58` → `60` | No verified sandbox; Flask signing not read from installed source by the verifier; who can read the repo is a deployment fact | Sign `{user_id: 2}` locally with the in-source key, `GET /notes` |

Owner-observed deployment check (key lead only): confirm whether any running instance uses the committed key value, by checking its configured `SECRET_KEY` or rotating it. No audit traffic should go to a deployment.

## Hardening notes and positive patterns

Hardening (not findings, no demonstrated boundary result):
- Passwords are stored and compared in plaintext (`seed.py:13,16`); hash them if the DB is ever disclosed.
- `POST /login` has no rate limit or lockout (`app.py:43-53`).
- `get_json(force=True)` accepts any content type, and a non-object body raises a 500 (`app.py:45`).
- No `SESSION_COOKIE_*` settings; Flask defaults are assumed from memory and were not verified in installed source.
- `current_user()` never checks that the user still exists, and there is no logout or revocation.
- No `.gitignore`, so `notes.db`, `uploads/` and `avatars/` could be committed by accident. Transitive dependencies are unpinned.
- `/avatars` is unauthenticated by design; keep the directory free of symlinks and non-public files.

Positive patterns seen in source:
- `POST /login` uses a parameterized query and a single 401 for all failures (`app.py:46-51`).
- `GET /notes` allow-lists `sort` through `SORT_COLUMNS` and binds `owner_id` (`app.py:19,59-62`).
- `/avatars` uses `send_from_directory` (`app.py:97`).
- `debug` is not enabled and the bind is `127.0.0.1` (`app.py:101`).

## Coverage summary (from `coverage-ledger.json`)

| Status | Units |
|---|---|
| candidate (linked to a `needs_validation` record) | 4 |
| covered | 0 (the three units hunters closed as covered were all reassigned by the critic, see below) |
| deferred (`quick_profile_final_critic`) | 4 |
| blocked | 0 |

Live counts: **4 candidate, 4 deferred, 0 covered, 0 blocked** (8 units).

Deferred units, none re-run because the quick profile allows exactly one hunter wave and one critic pass:
1. Browser-session unit (`POST /login` × `current_user`): reassigned. The critic noted `force=True` skips the Content-Type check, and the cross-site `text/plain` login and non-object body paths were not traced; Flask cookie defaults were from memory.
2. `Obvious things` application-wide checklist: reassigned. No dependency CVE lookup was done and transitive pins were not examined.
3. `/avatars` containment: reassigned. `safe_join` behavior was asserted from memory; installed Werkzeug source was not read by that hunter.
4. New unit `POST /login` request parsing (`get_json(force=True)`, `data.get`): proposed by the critic as an "Input handling and error paths" class that does not exist in `ATTACK-CLASSES.md`, so it was mapped to `Wildcard`.

The prior hunter evidence for the three reassigned units is archived in each unit's `attempts`.

**Final critic result:** one critic pass ran and returned `stop: false` with one missing unit and three reassignments. No clean-coverage claim is made.

## What would change this result

Approving a sandboxed run would let the four leads be reproduced. The verifier for the traversal lead found Flask 3.1.3 and Werkzeug 3.1.9 already present in a local uv cache, so no install should be needed. If the four reproduce, they become confirmed records with severities; the three deferred units and the login-parsing unit remain open for a second pass.
