# Security Audit: let Claude hunt for holes in your app

A hands-on tour of Cloudflare's [security-audit skill](https://github.com/cloudflare/security-audit-skill). You will point it at a tiny web app full of planted security bugs, read the report it writes, and score it against an answer key.

Everything below was run for real on 2026-10-22 with:

| Tool | Version |
|---|---|
| security-audit skill | commit `c1c8a8c` (2026-09-14), pinned by `setup.sh` |
| Skills CLI (`npx skills`, optional, for your own projects) | 1.7.4 |
| Claude Code | 2.1.309, model Sonnet |
| Node.js | 22.23.3 (the skill's validators need it; the skills CLI needs 22.20 or later) |
| Python / Flask (demo app only) | Python 3.14, Flask 3.1.3, uv 0.13.4 |

**Time:** 20-45 minutes. The audit itself took about 10 minutes. **Cost:** our run cost **$2.04** of Sonnet usage. It launches 11 helper agents, so it is the most expensive demo in this unit. Set a budget (Step 3 shows how).

> **Do not deploy the demo app.** `demo/leaky-notes/` is deliberately insecure. It only listens on 127.0.0.1, and you never need to start it as a server for this lesson.

## The idea in one paragraph

Ask a plain chatbot "is this code secure?" and you get a confident list that mixes real holes, generic advice ("add rate limiting!") and things that are not problems at all. This skill makes Claude behave like a careful security team instead. One agent maps the app. Separate "hunter" agents each search for one kind of attack. Then a **fresh** agent that did not find the bug tries to prove it wrong. Only bugs that survive, and that were actually reproduced, are labelled `confirmed` with a severity. Everything else is either `needs_validation` (a strong lead with the exact missing fact written down) or `rejected`. Cloudflare built it as the seed of their own vulnerability-hunting system, described in their blog post [Build your own vulnerability harness](https://blog.cloudflare.com/build-your-own-vulnerability-harness).

## What it does, in six phases

| Phase | What happens | File it produces |
|---|---|---|
| 1. Reconnaissance | 4 agents map the product, who can do what, every input, and what can be safely run | `architecture.md`, `coverage-ledger.json` |
| 2. Hunting | Hunter agents each take one "unit" (an input × a boundary × an attack type). A critic agent then looks for gaps | ledger updates |
| 3. Validation | Each candidate bug goes to a fresh verifier whose job is to disprove it | |
| 4. Structured output | Every verdict goes in a JSON file, checked by a validator script | `findings.json` |
| 5. Verification | Fresh agents re-check the final records (in the `quick` profile this merges with phase 3) | |
| 6. Report | Plain-English reports written from the verified records only | `REPORT.md`, `NEEDS-VALIDATION.md`, `FINDINGS-DETAIL.md` |

The skill has two modes. Asking a security *question* ("is this query safe?") uses **guidance mode**: no files, no six phases. Asking for a full audit ("do a security audit of this codebase") switches on **full audit mode**, which is what we demo.

## Is it safe to install?

It is a skill, so it is just instructions plus two small checker scripts (with their tests and a JSON schema). Before running it we read all of it:

- `SKILL.md` and 14 companion `.md` files: instructions only. None contain web links, `curl`, or install commands.
- `validate-findings.cjs` and `validate-coverage-ledger.cjs`: plain Node scripts that only *read* a JSON file and print PASS or a list of errors. No network, no shell commands.
- No hooks, no install script, no background process.

The skill itself tells the agent not to run the target's code unless an OS-level sandbox is in place. Keep that in mind: it explains the main surprise in the results.

## Setup

You need git, Node.js 22.20 or later (for the skill's checker scripts and the `npx skills` installer), Claude Code, and either [uv](https://docs.astral.sh/uv/) or Python 3.10+ with `venv` (only for the answer-key checker). On Windows, use WSL.

```bash
git clone https://github.com/vasuchettyphd/ai-dev-course.git
cd ai-dev-course/advanced/security-audit/demo
./setup.sh
```

`setup.sh` copies the demo app into `demo/practice/leaky-notes/` (git ignores `practice/`), makes it a git repo with one commit, and installs the skill **into that folder only**. It downloads the skill at commit `c1c8a8c`, the exact version this lesson was tested with, and copies it to `.claude/skills/security-audit/`. Expected output:

```
Created git repo at .../demo/practice/leaky-notes
Installed security-audit skill at commit c1c8a8c

Installed skill files:
AI-AND-LLM.md
ATTACK-CLASSES.md
...
SKILL.md
...
validate-findings.cjs
validate-findings.test.cjs

Next: cd .../demo/practice/leaky-notes && claude
```

Why not the usual `npx skills add` installer? It can only pin a branch or tag, not a single commit, so `setup.sh` fetches the commit with git instead. The result is the same folder of files.

**For your own projects later**, upstream's install command works from your project folder (it will ask which agent you use). It needs Node 22.20 or later:

```bash
DO_NOT_TRACK=1 npx -y skills@1.7.4 add https://github.com/cloudflare/security-audit-skill --skill security-audit
```

That installs the latest upstream version, not `c1c8a8c`. If Cloudflare has changed the skill since, your run may word things differently or produce different files. Add `--global` only if you want it in every project. `DO_NOT_TRACK=1` switches off the CLI's anonymous usage stats.

## The demo app: Leaky Notes

`demo/leaky-notes/app.py` is a 101-line Flask JSON API. Users log in, list and search their notes, view invoices, download attachments and fetch avatar pictures. Two dummy users exist: alice (id 1) and bob (id 2).

We planted **four real bugs and two decoys** (code that looks scary but is safe). Before you run anything, open `app.py` and make your own guess. Write down which lines you think are dangerous. The answer key is further down.

## Step-by-step demo

### Step 1: start Claude Code in the practice app

```bash
cd practice/leaky-notes
claude
```

Type `/` and then `security`. You should see `security-audit` in the list. That means the project-scoped skill loaded.

### Step 2: pick an output folder outside the app

By default the skill writes to `~/security-audit-skill/<repo>/run-<N>` in your home folder, and it refuses to write inside the audited repo unless git ignores that folder. We give it a folder next to `practice/` instead. Get the full path:

```bash
realpath ../../audit-output
```

### Step 3: ask for a quick audit with a budget

In Claude Code, type (swap in your path from Step 2):

> Do a full security audit of this codebase. Use the quick profile and a budget of 12 agent invocations. Write the audit output to /full/path/to/demo/audit-output/run-1.

- "full security audit" switches on full audit mode.
- **`quick` profile**: one hunting wave, one critic, one verifier per candidate. Right for a 100-line app.
- **budget of 12 agent invocations**: a hard cap on how many helper agents it may launch. Without one, a standard run on a big codebase can launch dozens.

Claude will ask permission for some shell commands (`mkdir`, `git`, `node`). Approve those. It will also try to check for Python, Flask and a sandbox tool called `bwrap`. **In our run we denied those**, so it ran no app code at all. See "What to notice" for why that matters.

<details>
<summary>Prefer to run it without the interactive UI? (this is exactly what we ran)</summary>

From `practice/leaky-notes`:

```bash
OUT="$(realpath ../../audit-output)"; mkdir -p "$OUT"
claude -p "Do a full security audit of this codebase. Use the quick profile and a budget of 12 agent invocations. Write the audit output to $OUT/run-1." \
  --model sonnet --permission-mode acceptEdits --add-dir "$OUT" --max-budget-usd 3 \
  --allowedTools "Read" "Grep" "Glob" "Write" "Edit" "Task" "Agent" \
  "Bash(node:*)" "Bash(git:*)" "Bash(mkdir:*)" "Bash(ls:*)"
```

Only the listed tools are allowed, so any attempt to run Python or `bwrap` is automatically denied.

</details>

### Step 4: watch it work

You will see it load the skill, then report progress like this (real lines from our run):

```
Four reconnaissance agents are running (4 of 12 invocations used).
Both hunters are running (6 of 12 invocations used).
The critic is running (7 of 12 invocations used). The four candidates go to fresh verifiers once it returns.
Four verifiers are running (11 of 12 invocations used, one left in reserve).
```

It finished with this summary (trimmed):

```
The quick-profile audit finished with 11 of 12 agent invocations used, but it found no
confirmed vulnerabilities. It found four strong leads that have not been reproduced.

I couldn't run anything: the shell needed approval for the bubblewrap and Flask checks,
so I never verified a sandbox. The audit rules require a bounded local result before a
finding counts as confirmed. So all four leads are `needs_validation`, with no severity
assigned. Each has a full source trace that a fresh verifier re-read independently.

| Lead                                                           | Where          |
|----------------------------------------------------------------|----------------|
| Hardcoded session key, so a session cookie could be forged     | app.py:17      |
| SQL injection in /notes/search                                 | app.py:71      |
| /attachments joins the user-supplied name onto the upload dir  | app.py:92      |
| /invoices/<id> has no ownership check                          | app.py:78-85   |

Coverage is partial. The final critic found a missing unit and flagged three units for
another look, but the quick profile allows no second hunter wave. Four units are
therefore deferred, and no unit is covered in the final ledger.
...
Both validators pass.
```

### Step 5: read the report

```bash
ls ../../audit-output/run-1
```

```
FINDINGS-DETAIL.md  NEEDS-VALIDATION.md  REPORT.md  agents  architecture.md  coverage-ledger.json  findings.json  run-metadata.json
```

Open `REPORT.md` first, then `NEEDS-VALIDATION.md`. If you skipped the run, our copies are in [`sample-output/`](sample-output/): [REPORT.md](sample-output/REPORT.md), [NEEDS-VALIDATION.md](sample-output/NEEDS-VALIDATION.md), [architecture.md](sample-output/architecture.md), [findings.json](sample-output/findings.json).

Each lead comes with a trace (where the input enters, where it ends up), the exact blocker, a safe local test plan and the smallest fix. For example, for the invoice bug:

```
- Trace: app.py:76 entrypoint (invoice_id is attacker-chosen) → 78 current_user() result
  discarded → 79 query by id only → 85 full row returned including owner_id.
- Local plan: log in as alice; GET /invoices/1 expects 200 with owner_id 1;
  GET /invoices/2 expects 200 with bob's Globex row if real, or 403/404 if refuted.
- Smallest fix: user_id = current_user() and WHERE id = ? AND owner_id = ? with 404 on no match.
```

You can re-run the skill's own format checks yourself:

```bash
node .claude/skills/security-audit/validate-findings.cjs ../../audit-output/run-1/findings.json
node .claude/skills/security-audit/validate-coverage-ledger.cjs ../../audit-output/run-1/coverage-ledger.json
```

```
PASS: 4 findings valid
PASS: 8 coverage units valid
```

PASS only means the files are well-formed. It says nothing about whether the bugs are real.

### Step 6: be the verifier yourself

The skill could not prove the bugs, so you will. `prove-bugs.sh` runs each attack against the app with Flask's built-in test client. No server, no port, no network. From the `demo/` folder:

```bash
cd ../..
./prove-bugs.sh
```

```
Seeded .../demo/practice/leaky-notes/notes.db
BUG 1 SQL injection (search):              ['Alice shopping list', 'Bob secret plans']
BUG 2 IDOR (invoice 2 as alice):           {'amount_cents': 990000, 'customer': 'Globex', 'id': 2, 'owner_id': 2}
BUG 3 path traversal (../app.py):          HTTP 200, first line: """Leaky Notes - a tiny invoice-and-notes app with planted security bugs.
BUG 4 forged cookie with known key:        ['Bob secret plans']
DECOY A sort=<injection attempt>:          HTTP 200, 1 note(s), table still there
DECOY B /avatars/../app.py:                HTTP 404 and 404 (blocked)
```

Alice, logged in as herself, sees bob's note, bob's invoice and the server's source code. An attacker with no password at all forges bob's login using the key in the source code. Each of the four leads is real.

## Answer key

Make your guess before opening this.

<details>
<summary>The four planted bugs, the two decoys, and how the skill scored</summary>

| # | Planted | Where | What an attacker gets | Skill's verdict |
|---|---|---|---|---|
| 1 | SQL injection | `app.py:71`, `q` pasted into the SQL with an f-string | Any user reads everyone's notes, and the `users` table with passwords | Found, `needs_validation` |
| 2 | IDOR (insecure direct object reference) | `app.py:76-85`, invoice looked up by id only | Any user reads any invoice by changing the number in the URL | Found, `needs_validation` ("least remaining doubt") |
| 3 | Path traversal | `app.py:92`, `os.path.join(UPLOAD_DIR, name)` into `send_file` | Read any file the server can read: source code, `notes.db` | Found, `needs_validation` |
| 4 | Hard-coded secret | `app.py:17`, `app.secret_key = "..."` | Anyone who has seen the code can sign a login cookie for any user | Found, `needs_validation` |
| A | Decoy: f-string SQL in `ORDER BY` | `app.py:59-62` | Nothing: only the three fixed values in `SORT_COLUMNS` can ever reach the SQL | Listed under **positive patterns**, not a finding |
| B | Decoy: user-controlled path in `/avatars` | `app.py:95-97` | Nothing: `send_from_directory` refuses to leave the folder | Listed as a positive pattern, but its unit was **deferred** (see below) |

**Score: 4 of 4 real bugs found, 0 false positives, 0 confirmed.** Plus seven hardening notes (plaintext passwords, no login rate limit, and so on), kept separate from findings.

</details>

## What to notice

1. **Zero "confirmed" is the honest answer here, not a failure.** The skill's rule is: no reproduction, no severity. We gave it no sandbox and no permission to run Python, so it stopped at "strong lead" and wrote down exactly what test would settle each one. A sloppy auditor would have labelled all four "CRITICAL" from reading alone. When you ran `prove-bugs.sh` you did phase 3's job by hand, and every test plan it wrote matched what we ran.
2. **The decoys are why verification exists.** Decoy A has the same scary shape as bug 1: SQL built with an f-string. A pattern-matching scanner flags both. The skill traced where the value comes from, saw the allowlist, and called it a good pattern. That is the difference between "looks dangerous" and "is dangerous".
3. **It is honest about what it did not check.** For decoy B, the critic agent noticed the hunter had claimed `send_from_directory` is safe "from memory" without reading Flask's actual code. Instead of accepting that, it marked the unit `deferred`. The report says plainly: "No clean-coverage claim is made."
4. **Hardening notes are not findings.** Plaintext passwords and no rate limit are real weaknesses, but none crosses a boundary on its own in this app. The skill puts them in a separate list. Good security reports keep "you have been robbed" apart from "you should lock the back door".
5. **One pass is never the whole story.** Upstream says a single run found roughly half of what repeated runs found. Our quick run left four units deferred. A second run reads the earlier ledger and targets the gaps.

## Limits and caveats

- **Cost and time.** $2.04 and about 10 minutes for 100 lines of code. A real codebase on the `standard` profile costs far more. Always set a budget, or start with a scoped run ("audit only `src/payments`").
- **Confirming bugs needs a real sandbox**: no network, read-only code, a clean environment and resource limits (for example `bwrap` on Linux). We did not test a run with a sandbox, so we cannot show what "confirmed" output looks like. Upstream says that without one, every lead stays `needs_validation`.
- **It is not a guarantee.** No findings does not mean secure, and the report says so. Treat it as a very thorough reviewer, not a certificate.
- **The demo app is labelled "deliberately vulnerable"** in its docstring, and the agent read that. It still traced each bug from the code, but on your own projects there is no such hint.
- **It wanders a little.** In our run one verifier read Flask's source from the local uv cache in the home folder (read-only), and the main agent wrote two small helper scripts (`ledger-update-1.cjs`, `ledger-update-2.cjs`) into `demo/`, outside the output folder. The lesson's `.gitignore` ignores them. Neither is harmful, but it shows why you review what an agent touches.
- **Only audit code you own or have permission to test.** The skill never probes live servers, and neither should you.

## Troubleshooting

| Problem | Fix |
|---|---|
| `practice/leaky-notes already exists` | Run `./reset.sh`, then `./setup.sh` again |
| `security-audit` does not appear when you type `/` | Make sure you started `claude` inside `practice/leaky-notes`. Check `.claude/skills/security-audit/SKILL.md` exists |
| Claude answers in chat and writes no files | That is guidance mode. Say "full security audit" and give an output folder |
| It stops and asks for an output folder | It will not write inside the repo it audits. Give it the `audit-output` path from Step 2 |
| `./prove-bugs.sh` says `ensurepip is not available` | Install uv (recommended) or your system's `python3-venv` package, then retry |
| Run gets expensive | Lower the budget in your prompt, or add `--max-budget-usd` when using `claude -p` |

## Clean up

From the folder where you cloned the course:

```bash
cd ai-dev-course/advanced/security-audit/demo
./reset.sh          # deletes practice/ (app copy + project-scoped skill) and audit-output/
rm -f *.cjs         # helper scripts the agent may have left behind
```

If you ran an audit without naming an output folder, also delete `~/security-audit-skill/`.

If you installed the skill in another project, remove it from there with:

```bash
DO_NOT_TRACK=1 npx -y skills@1.7.4 remove security-audit
```

(add `--global` if you installed it globally), or simply delete that project's `.claude/skills/security-audit/` folder.

## Files

| Path | What it is |
|---|---|
| `demo/leaky-notes/` | The deliberately vulnerable app (`app.py`, `seed.py`, `requirements.txt`). Do not deploy |
| `demo/setup.sh` | Copies the app to `demo/practice/`, makes it a git repo, installs the skill (pinned to `c1c8a8c`) there |
| `demo/prove-bugs.sh`, `demo/prove_bugs.py` | Answer-key checker using Flask's test client |
| `demo/reset.sh` | Deletes `practice/` and `audit-output/` |
| `sample-output/` | The report files from our run (`REPORT.md`, `NEEDS-VALIDATION.md`, `FINDINGS-DETAIL.md`, `architecture.md`, `findings.json`), so you can read them without paying for a run |
| `.gitignore` | Keeps `demo/practice/`, `demo/audit-output/`, runtime files and stray agent scripts out of git |
| `README.md` | This lesson |
