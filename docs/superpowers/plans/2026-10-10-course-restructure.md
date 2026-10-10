# Course Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure `ai-dev-course` into the 14-week course layout. This covers week stubs, `advanced/`, the syllabus, a Marp slide build, a course checker, and the private instructor repo. No week content is written yet.

**Architecture:**
- **Content:** plain Markdown, with three files per week following templates.
- **Checker:** a stdlib-only Python script, `scripts/check_course.py`, enforces the layout, the no-em-dash rule, rubric totals and relative links. Every later week PR runs it.
- **Slides:** Marp CLI builds every `slides.md` into a `slides.pdf`, which is committed so students who don't code get PDFs without installing anything.

**Tech Stack:** Markdown, Python 3 (stdlib `unittest`), Node 22 + `@marp-team/marp-cli` 4.1.2, git.

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`

**Out of this plan:** the content of weeks 1-14. Each week gets its own plan, written when that week is started, using the templates and checker built here.

## Global Constraints

- No em dashes (U+2014) in any file, including code, comments and copy. Use "-" instead.
- Never commit to `main`. Work on a branch and open a PR. Ask the user to merge in the GitHub UI, because auto mode blocks merges.
- PRs in this repo are squash-merged. (The history-preserving merge was a one-off exception.)
- Week folder names are exactly: `01-what-is-ai`, `02-claude-code-setup`, `03-git-and-github`, `04-planning`, `05-building-with-ai`, `06-reviewing-code`, `07-running-with-docker`, `08-debugging`, `09-calling-a-model`, `10-embeddings-and-rag`, `11-tools-agents-mcp`, `12-evaluation`, `13-security-and-responsible-use`, `14-final-demos`.
- Advanced folder names are exactly: `dbt`, `local-llm-docker`, `jev`, `wordle-agent`, `grill-me-superpowers`, `beads`.
- Rubrics total 10 points in weeks 1-13 and 30 points in week 14.
- Student costs, stated verbatim in the syllabus: Claude Pro about $20/month, plus about $5 of one-time API credit for weeks 9-11.
- The instructor repo is private: `vasuchettyphd/ai-dev-course-instructor`.
- Log work in OpenProject project id 4 (Tutorials and Teaching).

## Review Focus

1. **Old paths after the move.** A student copies `cd ai-dev-course/01-dbt` from a README that still uses the old numbering. Every clone and `cd` path must use `advanced/<name>`. Task 2 adds a checker test that fails on any `0[1-6]-` tutorial path.
2. **Windows line endings break shell scripts.** A student clones on the Windows side and runs `06-beads/scripts/*.sh` in WSL, and gets `\r: command not found`. Task 2 adds `.gitattributes` with `*.sh text eol=lf`, and a checker test that every `.sh` file is covered by it.
3. **A stub week looks finished.** A student opens a week on GitHub before its content exists. Each stub must say plainly that it is coming soon. Task 1's checker treats a README containing `Status: coming soon` as a stub, so it isn't required to have slides or an assignment.
4. **The PDF build fails because no browser is installed.** Marp needs Chrome, Edge or Firefox. Task 4 verifies the build on this machine and documents the fallback (`--browser firefox`) in `CONTRIBUTING.md`.
5. **Em dashes slip in through pasted content.** A tutorial gets text pasted from elsewhere. The checker scans every tracked text file, and Task 1 tests that it catches one.

---

### Task 1: Course checker

**Files:**
- Create: `scripts/check_course.py`
- Create: `scripts/test_check_course.py`

**Interfaces:**
- Produces: `python3 scripts/check_course.py [root]` exits 0 and prints `OK` when clean. Otherwise it exits 1 and prints one `path: problem` line per issue. Functions: `check(root: pathlib.Path) -> list[str]`, `WEEKS: list[str]`, `ADVANCED: list[str]`.

- [ ] **Step 1: Write the failing tests**

```python
# scripts/test_check_course.py
import pathlib, tempfile, unittest
from check_course import check, WEEKS, ADVANCED

STUB = "# Week\n\nStatus: coming soon\n"
RUBRIC10 = "| Criterion | Points |\n|---|---|\n| Works | 6 |\n| Explained | 4 |\n"
RUBRIC30 = "| Criterion | Points |\n|---|---|\n| Demo | 20 |\n| Write-up | 10 |\n"


def make_course(root):
    for w in WEEKS:
        (root / "weeks" / w).mkdir(parents=True)
        (root / "weeks" / w / "README.md").write_text(STUB)
    for a in ADVANCED:
        (root / "advanced" / a).mkdir(parents=True)
        (root / "advanced" / a / "README.md").write_text("# T\n")
    (root / "README.md").write_text("# Course\n")
    (root / ".gitattributes").write_text("*.sh text eol=lf\n")


class CheckCourse(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        make_course(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_course_passes(self):
        self.assertEqual(check(self.root), [])

    def test_missing_week_folder(self):
        (self.root / "weeks" / "05-building-with-ai" / "README.md").unlink()
        (self.root / "weeks" / "05-building-with-ai").rmdir()
        self.assertTrue(any("05-building-with-ai" in p for p in check(self.root)))

    def test_finished_week_needs_slides_and_assignment(self):
        (self.root / "weeks" / "01-what-is-ai" / "README.md").write_text("# Week 1\n")
        problems = check(self.root)
        self.assertTrue(any("slides.md" in p for p in problems))
        self.assertTrue(any("assignment.md" in p for p in problems))

    def test_rubric_must_total_10(self):
        w = self.root / "weeks" / "01-what-is-ai"
        (w / "README.md").write_text("# Week 1\n")
        (w / "slides.md").write_text("# s\n")
        (w / "assignment.md").write_text(RUBRIC10.replace("| 4 |", "| 3 |"))
        self.assertTrue(any("total 9" in p for p in check(self.root)))
        (w / "assignment.md").write_text(RUBRIC10)
        self.assertEqual(check(self.root), [])

    def test_week_14_rubric_totals_30(self):
        w = self.root / "weeks" / "14-final-demos"
        (w / "README.md").write_text("# Week 14\n")
        (w / "slides.md").write_text("# s\n")
        (w / "assignment.md").write_text(RUBRIC30)
        self.assertEqual(check(self.root), [])

    def test_em_dash_caught_anywhere(self):
        (self.root / "advanced" / "dbt" / "notes.py").write_text("x = 1  # a \u2014 b\n")
        self.assertTrue(any("em dash" in p for p in check(self.root)))

    def test_broken_relative_link(self):
        (self.root / "README.md").write_text("[w](weeks/99-nope/)\n[ok](weeks/01-what-is-ai/)\n[web](https://x.y)\n")
        problems = check(self.root)
        self.assertEqual(len(problems), 1)
        self.assertIn("weeks/99-nope/", problems[0])

    def test_old_numbered_tutorial_path(self):
        (self.root / "advanced" / "dbt" / "README.md").write_text("cd ai-dev-course/01-dbt\n")
        self.assertTrue(any("old path" in p for p in check(self.root)))

    def test_docs_may_mention_old_paths_and_example_links(self):
        (self.root / "docs").mkdir()
        (self.root / "docs" / "plan.md").write_text("Move `01-dbt`, see [x](weeks/99-nope/)\n")
        self.assertEqual(check(self.root), [])

    def test_shell_scripts_need_lf_rule(self):
        (self.root / ".gitattributes").write_text("")
        (self.root / "advanced" / "beads" / "run.sh").write_text("echo hi\n")
        self.assertTrue(any("eol=lf" in p for p in check(self.root)))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to check they fail**

Run: `cd scripts && python3 -m unittest test_check_course -v`
Expected: `ModuleNotFoundError: No module named 'check_course'`

- [ ] **Step 3: Write the checker**

```python
# scripts/check_course.py
"""Check the course layout and style rules. Usage: python3 scripts/check_course.py [root]"""
import pathlib, re, sys

WEEKS = [
    "01-what-is-ai", "02-claude-code-setup", "03-git-and-github", "04-planning",
    "05-building-with-ai", "06-reviewing-code", "07-running-with-docker", "08-debugging",
    "09-calling-a-model", "10-embeddings-and-rag", "11-tools-agents-mcp", "12-evaluation",
    "13-security-and-responsible-use", "14-final-demos",
]
ADVANCED = ["dbt", "local-llm-docker", "jev", "wordle-agent", "grill-me-superpowers", "beads"]
TEXT = {".md", ".py", ".sh", ".json", ".yml", ".yaml", ".sql", ".txt", ".html", ".js", ".css", ".toml", ".csv"}
SKIP = {".git", "node_modules", "__pycache__", ".venv", "venv"}
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
OLD_PATH = re.compile(r"\b0[1-6]-(dbt|local-llm-docker|jev|wordle-agent|grill-me-superpowers|beads)\b")
POINTS = re.compile(r"^\|[^|]+\|\s*(\d+)\s*\|\s*$")


def files(root):
    for p in sorted(root.rglob("*")):
        if p.is_file() and not SKIP & set(p.relative_to(root).parts):
            yield p


def rubric_total(text):
    return sum(int(m.group(1)) for line in text.splitlines() if (m := POINTS.match(line.strip())))


def check(root):
    root = pathlib.Path(root)
    problems = []
    for w in WEEKS:
        d = root / "weeks" / w
        readme = d / "README.md"
        if not readme.is_file():
            problems.append(f"weeks/{w}: missing README.md")
            continue
        if "Status: coming soon" in readme.read_text():
            continue
        for name in ("slides.md", "assignment.md"):
            if not (d / name).is_file():
                problems.append(f"weeks/{w}: missing {name}")
        a = d / "assignment.md"
        if a.is_file():
            want = 30 if w == "14-final-demos" else 10
            got = rubric_total(a.read_text())
            if got != want:
                problems.append(f"weeks/{w}/assignment.md: rubric total {got}, expected {want}")
    for a in ADVANCED:
        if not (root / "advanced" / a / "README.md").is_file():
            problems.append(f"advanced/{a}: missing README.md")
    attrs = root / ".gitattributes"
    lf_rule = attrs.is_file() and "*.sh text eol=lf" in attrs.read_text()
    for p in files(root):
        rel = p.relative_to(root)
        if p.suffix == ".sh" and not lf_rule:
            problems.append(f"{rel}: shell script not covered by '*.sh text eol=lf' in .gitattributes")
        if p.suffix not in TEXT:
            continue
        text = p.read_text(errors="replace")
        if "\u2014" in text:
            problems.append(f"{rel}: contains an em dash")
        if p.suffix == ".md" and rel.parts[0] != "docs":
            for m in OLD_PATH.finditer(text):
                problems.append(f"{rel}: old path '{m.group(0)}', use advanced/{m.group(1)}")
            for target in LINK.findall(text):
                if re.match(r"^[a-z]+:", target):
                    continue
                if not (p.parent / target).exists():
                    problems.append(f"{rel}: broken link {target}")
    return problems


if __name__ == "__main__":
    found = check(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."))
    print("\n".join(found) if found else "OK")
    sys.exit(1 if found else 0)
```

- [ ] **Step 4: Run the tests to check they pass**

Run: `cd scripts && python3 -m unittest test_check_course -v`
Expected: 10 tests, `OK`

- [ ] **Step 5: Commit**

```bash
git add scripts/check_course.py scripts/test_check_course.py
git commit -m "Add course checker for layout, rubrics, links and em dashes"
```

### Task 2: Move the six tutorials to advanced/

**Files:**
- Move: `01-dbt` to `advanced/dbt`, `02-local-llm-docker` to `advanced/local-llm-docker`, `03-jev` to `advanced/jev`, `04-wordle-agent` to `advanced/wordle-agent`, `05-grill-me-superpowers` to `advanced/grill-me-superpowers`, `06-beads` to `advanced/beads`
- Modify: `advanced/dbt/README.md`, `advanced/local-llm-docker/README.md`, `advanced/beads/README.md` (the `cd ai-dev-course/0N-...` lines)
- Create: `.gitattributes`

**Interfaces:**
- Consumes: `scripts/check_course.py` from Task 1.
- Produces: the `advanced/<name>/` paths that Task 3's syllabus links to.

- [ ] **Step 1: Move the folders, keeping their history**

```bash
mkdir -p advanced
git mv 01-dbt advanced/dbt
git mv 02-local-llm-docker advanced/local-llm-docker
git mv 03-jev advanced/jev
git mv 04-wordle-agent advanced/wordle-agent
git mv 05-grill-me-superpowers advanced/grill-me-superpowers
git mv 06-beads advanced/beads
```

- [ ] **Step 2: Run the checker to see the old paths it reports**

Run: `python3 scripts/check_course.py`
Expected: exit 1. Lines include `advanced/dbt/README.md: old path '01-dbt'`, `advanced/local-llm-docker/README.md: old path '02-local-llm-docker'` and `advanced/beads/README.md: old path '06-beads'`. There are also `missing README.md` lines for the 14 weeks (Task 3 fixes those) and shell-script `eol=lf` lines for `advanced/beads`.

- [ ] **Step 3: Fix the paths and add .gitattributes**

```bash
sed -i 's#cd ai-dev-course/01-dbt#cd ai-dev-course/advanced/dbt#' advanced/dbt/README.md
sed -i 's#cd ai-dev-course/02-local-llm-docker#cd ai-dev-course/advanced/local-llm-docker#; s#^02-local-llm-docker/$#local-llm-docker/#' advanced/local-llm-docker/README.md
sed -i 's#cd ai-dev-course/06-beads#cd ai-dev-course/advanced/beads#' advanced/beads/README.md
printf '# Shell scripts must keep Unix line endings, even when cloned on Windows\n*.sh text eol=lf\n' > .gitattributes
```

- [ ] **Step 4: Check that only the week READMEs are still reported**

Run: `python3 scripts/check_course.py | grep -v '^weeks/'`
Expected: no output. If it reports a `broken link` inside one of the six tutorials, that link was already broken before the move. Fix it if the right target is obvious from the folder contents. If not, report it to the user rather than guessing.

Run: `cd advanced/jev/experiments && python3 -m unittest test_truth`
Expected: `OK` (the moved tutorial still works).

- [ ] **Step 5: Commit**

```bash
git add -A advanced .gitattributes
git commit -m "Move the six tutorials to advanced/ and keep shell scripts LF"
```

### Task 3: Week stubs, templates and syllabus

**Files:**
- Create: `weeks/<each of the 14 names>/README.md` (stub)
- Create: `templates/README.md`, `templates/slides.md`, `templates/assignment.md`
- Modify: `README.md` (rewrite as the syllabus)

**Interfaces:**
- Consumes: the `advanced/<name>/` paths from Task 2, and `WEEKS` from Task 1.
- Produces: `templates/*`, which every week plan copies; and the stub marker `Status: coming soon`, which the checker treats as unfinished.

- [ ] **Step 1: Create the 14 stubs**

```bash
python3 - <<'EOF'
import pathlib
titles = {
 "01-what-is-ai": "What AI is", "02-claude-code-setup": "Setting up Claude Code",
 "03-git-and-github": "Git and GitHub", "04-planning": "Planning a project",
 "05-building-with-ai": "Building with AI", "06-reviewing-code": "Reviewing code",
 "07-running-with-docker": "Running what you build", "08-debugging": "Debugging with AI",
 "09-calling-a-model": "Calling a model from code", "10-embeddings-and-rag": "Embeddings and RAG",
 "11-tools-agents-mcp": "Tools, agents and MCP", "12-evaluation": "Evaluation",
 "13-security-and-responsible-use": "Security and responsible use", "14-final-demos": "Final demos",
}
for i, (folder, title) in enumerate(titles.items(), 1):
    d = pathlib.Path("weeks") / folder
    d.mkdir(parents=True, exist_ok=True)
    (d / "README.md").write_text(
        f"# Week {i}: {title}\n\nStatus: coming soon\n\n"
        "This week's tutorial, slides and assignment haven't been published yet. "
        "Check back before the class session, or see the [course schedule](../../README.md).\n")
EOF
```

- [ ] **Step 2: Write the three templates**

`templates/README.md`:
```markdown
# Week N: Title

**Goal:** one sentence on what you can do by the end of this week.

**Time:** about N minutes. **Cost:** what this week costs, or "nothing beyond your Claude plan".

**Tested with:** tool name and version, date.

## Before you start

What you need from earlier weeks.

## Steps

### 1. First step

What to do, the exact command, and what you should see.

## Check it worked

How to tell it worked.

## Troubleshooting

| What you see | What to do |
|---|---|
| error text | fix |
```

`templates/slides.md`:
```markdown
---
marp: true
paginate: true
title: Week N - Title
---

# Week N: Title

AI Development Course

---

## Today

- Idea one
- Idea two
- Hands-on: follow the week's README
```

`templates/assignment.md`:
```markdown
# Week N assignment: Title

## What to do

Apply this week's work to your own project.

## What to hand in

- Item

## Rubric

| Criterion | Points |
|---|---|
| It works | 4 |
| You can explain it | 3 |
| It follows the week's method | 3 |
```

- [ ] **Step 3: Rewrite README.md as the syllabus**

```markdown
# AI Development Course

A 14-week, hands-on course at Utah Valley University on building useful tools with AI, for students with little or no coding experience. You'll learn how modern AI works, set up Claude Code, and spend the semester building a small AI-powered tool of your own: planning it, building it, reviewing it, running it, then adding AI features and measuring how well they work.

## Get the course

    git clone https://github.com/vasuchettyphd/ai-dev-course.git
    cd ai-dev-course

Each week lives in its own folder. Follow that week's README from inside the folder.

## Costs

- **Claude Pro, about $20/month**, for Claude Code. Week 2 walks you through signing up.
- **About $5 of one-time API credit**, used in weeks 9-11 when your own code calls a model. Claude Pro doesn't cover this.

## Before week 1

A laptop running macOS, or Windows 10/11 (we'll set up WSL together in week 2). Nothing else needs installing yet.

## Schedule

| Week | Topic |
|---|---|
| 1 | [What AI is](weeks/01-what-is-ai/) |
| 2 | [Setting up Claude Code](weeks/02-claude-code-setup/) |
| 3 | [Git and GitHub](weeks/03-git-and-github/) |
| 4 | [Planning a project](weeks/04-planning/) |
| 5 | [Building with AI](weeks/05-building-with-ai/) |
| 6 | [Reviewing code](weeks/06-reviewing-code/) |
| 7 | [Running what you build](weeks/07-running-with-docker/) |
| 8 | [Debugging with AI, and midterm check-in](weeks/08-debugging/) |
| 9 | [Calling a model from code](weeks/09-calling-a-model/) |
| 10 | [Embeddings and RAG](weeks/10-embeddings-and-rag/) |
| 11 | [Tools, agents and MCP](weeks/11-tools-agents-mcp/) |
| 12 | [Evaluation](weeks/12-evaluation/) |
| 13 | [Security and responsible use](weeks/13-security-and-responsible-use/) |
| 14 | [Final demos](weeks/14-final-demos/) |

## Your project

In week 4 you choose a small tool to build, something useful for your work, studies or a business idea. Every week after that you apply what you learned to it, and in week 14 you demo it. The class examples use a shared project, a rental property deal screener, and its state at the end of each week is tagged in `example-project/`.

## Grading

Weeks 1-13 each have a 10-point assignment with a rubric in that week's `assignment.md`. The final project in week 14 is worth 30 points.

## Advanced topics

Optional, for after the core course or for extra credit. Each one stands alone.

| Topic | What you learn |
|---|---|
| [dbt with Postgres](advanced/dbt/) | Turn raw CSV data into tested tables with dbt |
| [Run an LLM locally](advanced/local-llm-docker/) | Serve an open model in Docker (needs an NVIDIA GPU) |
| [Jev](advanced/jev/) | Measure where a narrow classifier is reliable (week 12's case study) |
| [Wordle agent](advanced/wordle-agent/) | Build an agent with one tool and a validator it can't fake |
| [`/grill-me` and Superpowers in depth](advanced/grill-me-superpowers/) | The full rental deal screener walkthrough |
| [Beads](advanced/beads/) | Keep an agent's task list across sessions (optional in week 5) |

## History

The advanced tutorials started as separate repositories and keep their full commit history here. Run `git log --follow advanced/<name>/README.md` to see how one was built.
```

Note that the week 14 rubric (30 points) and the costs come verbatim from Global Constraints. The syllabus does not link `example-project/`, because that folder is created in week 4's plan. Keep it as plain code text so the link checker passes.

- [ ] **Step 4: Run the checker**

Run: `python3 scripts/check_course.py`
Expected: `OK`, exit 0.

- [ ] **Step 5: Commit**

```bash
git add weeks templates README.md
git commit -m "Add week stubs, week templates and the course syllabus"
```

### Task 4: Slide build

**Files:**
- Create: `package.json`, `CONTRIBUTING.md`
- Modify: `.gitignore` (add `node_modules/`)

**Interfaces:**
- Consumes: `templates/slides.md` from Task 3.
- Produces: `npm run slides`, which builds every `weeks/*/slides.md` into a `slides.pdf` next to it. Week plans run it before committing.

- [ ] **Step 1: Check that the build fails before setup**

Run: `npm run slides`
Expected: `npm error Missing script: "slides"` (or no package.json found).

- [ ] **Step 2: Add package.json and the ignore rule**

```json
{
  "name": "ai-dev-course",
  "private": true,
  "description": "Build tooling for the course slides",
  "scripts": {
    "slides": "sh -c 'set -- weeks/*/slides.md; [ -e \"$1\" ] || { echo \"no slides yet\"; exit 0; }; marp --pdf --allow-local-files \"$@\"'",
    "slides:template": "marp --pdf --allow-local-files templates/slides.md -o /tmp/template-check.pdf"
  },
  "devDependencies": {
    "@marp-team/marp-cli": "4.1.2"
  }
}
```

```bash
printf 'node_modules/\n' >> .gitignore
npm install
```

- [ ] **Step 3: Build the template deck to prove the toolchain works**

Run: `npm run slides:template && file /tmp/template-check.pdf`
Expected: `/tmp/template-check.pdf: PDF document`.

If it fails with "No suitable browser found", run `npx marp --pdf --browser firefox templates/slides.md -o /tmp/template-check.pdf`. If that works, add `--browser firefox` to both scripts. If no browser is installed at all, stop and report it: installing Chromium in WSL is the user's call.

Run: `npm run slides`
Expected: prints `no slides yet` and exits 0. (With several input files, Marp writes each `slides.pdf` next to its `slides.md`, and only `slides.md` files are built, never READMEs or assignments.)

- [ ] **Step 4: Write CONTRIBUTING.md**

```markdown
# Working on the course

- **New week:** copy the three files in `templates/` into the week folder and remove the `Status: coming soon` line from its README.
- **Slides:** run `npm install` once, then `npm run slides` to build every `weeks/*/slides.md` into `slides.pdf`. Commit the PDF as well, so students can open it without installing anything. If Marp can't find a browser, add `--browser firefox` to the scripts in `package.json`.
- **Before every PR:** run `python3 scripts/check_course.py`. It must print `OK`. It checks the week layout, rubric totals (10 points, or 30 for week 14), relative links, old tutorial paths, shell-script line endings and em dashes.
- **Style:** plain language for students who don't code, every command shown with its expected output, the tested tool versions listed at the top, and no em dashes.
```

- [ ] **Step 5: Run the checker and commit**

Run: `python3 scripts/check_course.py`
Expected: `OK`

```bash
git add package.json package-lock.json .gitignore CONTRIBUTING.md
git commit -m "Add Marp slide build and contributor notes"
```

### Task 5: Private instructor repo

**Files (new repo `~/claude/ai-dev-course-instructor`):**
- Create: `README.md`, `weeks/<each of the 14 names>/notes.md`

**Interfaces:**
- Consumes: the week names from Global Constraints.
- Produces: `weeks/<name>/notes.md` with the headings `## Timing`, `## Common problems`, `## Discussion answers`, `## Grading guidance`, which every week plan fills in.

- [ ] **Step 1: Create the private GitHub repo**

Use `mcp__plugin_github_github__create_repository` with name `ai-dev-course-instructor`, `private: true`, `autoInit: false`, and description `Instructor notes for ai-dev-course (private)`.
Expected: the repo URL is returned.

- [ ] **Step 2: Create the local repo with stubs**

```bash
mkdir ~/claude/ai-dev-course-instructor && cd ~/claude/ai-dev-course-instructor
git init -q -b add-week-stubs
python3 - <<'EOF'
import pathlib
weeks = ["01-what-is-ai","02-claude-code-setup","03-git-and-github","04-planning","05-building-with-ai","06-reviewing-code","07-running-with-docker","08-debugging","09-calling-a-model","10-embeddings-and-rag","11-tools-agents-mcp","12-evaluation","13-security-and-responsible-use","14-final-demos"]
for i, w in enumerate(weeks, 1):
    d = pathlib.Path("weeks") / w
    d.mkdir(parents=True)
    (d / "notes.md").write_text(f"# Week {i} instructor notes\n\nStatus: not written yet\n\n## Timing\n\n## Common problems\n\n## Discussion answers\n\n## Grading guidance\n")
pathlib.Path("README.md").write_text("# AI Development Course: instructor notes\n\nPrivate. One folder per week, matching the public repo vasuchettyphd/ai-dev-course. Never copy answers or grading guidance into the public repo.\n")
EOF
grep -rc $'\u2014' . --include=*.md | grep -v ':0' ; echo "em-dash check done"
```

Expected: `em-dash check done`, with no file listed before it.

- [ ] **Step 3: Bootstrap main and open the PR**

Bootstrap `main` by PUT-ing `README.md` to the contents API on branch `main`. Use the same content as the local file, so the later merge has no conflict. Then:

```bash
git add -A && git commit -qm "Add instructor note stubs for the 14 weeks"
git remote add origin https://github.com/vasuchettyphd/ai-dev-course-instructor.git
git fetch -q origin && git merge -q --allow-unrelated-histories --no-edit origin/main
git push -u origin add-week-stubs
```

Open the PR with the `github:gh-create-pr` skill, and ask the user to squash-merge it in the GitHub UI.

### Task 6: Course repo PR

- [ ] **Step 1: Final checks on the branch**

Run: `python3 scripts/check_course.py && (cd scripts && python3 -m unittest test_check_course) && (cd advanced/jev/experiments && python3 -m unittest test_truth)`
Expected: `OK` three times.

Run: `git log --follow --oneline advanced/beads/README.md | wc -l`
Expected: 4 or more (the history survived the move).

- [ ] **Step 2: Push and open the PR**

Push branch `docs/course-design`, which holds the spec, this plan and Tasks 1-4. Open a PR with `github:gh-create-pr`, then ask the user to squash-merge it in the GitHub UI.

- [ ] **Step 3: Record the work**

Create and close an OpenProject task in project 4: "Restructure ai-dev-course into 14-week course layout". Update the `ai-dev-course` memory: weeks live in `weeks/`, the six tutorials in `advanced/`, the templates in `templates/`, and the checker is `scripts/check_course.py`.

## Amendments during execution

- Checker hardening: UTF-8 reads, skipping dot-directories, notebooks, links inside code ignored, URL forms, Total rows ignored, file list from `git ls-files`, an em-dash scan that does not depend on file suffix, and the rubric read from the table under `## Rubric`.
- Slides are built with Marp in Docker (`marpteam/marp-cli:v4.1.2`) instead of an npm dependency, by the user's choice.
- History is checked by ancestry and shown with `git log --graph --oneline`, because `--follow` cannot reach subtree-imported history.
- The GitHub steps for the instructor repo were done by the controller.
