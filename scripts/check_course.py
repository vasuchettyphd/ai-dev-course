# scripts/check_course.py
"""Check the course layout and style rules. Usage: python3 scripts/check_course.py [root]"""
import pathlib, re, sys, urllib.parse

WEEKS = [
    "01-what-is-ai", "02-claude-code-setup", "03-git-and-github", "04-planning",
    "05-building-with-ai", "06-reviewing-code", "07-running-with-docker", "08-debugging",
    "09-calling-a-model", "10-embeddings-and-rag", "11-tools-agents-mcp", "12-evaluation",
    "13-security-and-responsible-use", "14-final-demos",
]
ADVANCED = ["dbt", "local-llm-docker", "jev", "wordle-agent", "grill-me-superpowers", "beads"]
TEXT = {".md", ".py", ".sh", ".json", ".yml", ".yaml", ".sql", ".txt", ".html", ".js", ".css", ".toml", ".csv", ".ipynb"}
SKIP = {".git", "node_modules", "__pycache__", ".venv", "venv"}
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
FENCE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
OLD_PATH = re.compile(r"\b0[1-6]-(dbt|local-llm-docker|jev|wordle-agent|grill-me-superpowers|beads)\b")
POINTS = re.compile(r"^\|[^|]+\|\s*(\d+)\s*\|\s*$")


def read(p):
    return p.read_text(encoding="utf-8", errors="replace")


def files(root):
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        parts = p.relative_to(root).parts
        if any(part in SKIP for part in parts):
            continue
        if any(part.startswith(".") for part in parts[:-1]):
            continue
        yield p


def rubric_total(text):
    total = 0
    for line in text.splitlines():
        m = POINTS.match(line.strip())
        if not m:
            continue
        first_cell = line.strip().strip("|").split("|")[0].strip().lower()
        if first_cell != "total":
            total += int(m.group(1))
    return total


def link_targets(text):
    text = INLINE_CODE.sub("", FENCE.sub("", text))
    for raw in LINK.findall(text):
        if SCHEME.match(raw):
            continue
        yield urllib.parse.unquote(raw.split("?")[0])


def check(root):
    root = pathlib.Path(root)
    problems = []
    for w in WEEKS:
        d = root / "weeks" / w
        readme = d / "README.md"
        if not readme.is_file():
            problems.append(f"weeks/{w}: missing README.md")
            continue
        if "Status: coming soon" in read(readme):
            continue
        for name in ("slides.md", "assignment.md"):
            if not (d / name).is_file():
                problems.append(f"weeks/{w}: missing {name}")
        a = d / "assignment.md"
        if a.is_file():
            want = 30 if w == "14-final-demos" else 10
            got = rubric_total(read(a))
            if got != want:
                problems.append(f"weeks/{w}/assignment.md: rubric total {got}, expected {want}")
    for a in ADVANCED:
        if not (root / "advanced" / a / "README.md").is_file():
            problems.append(f"advanced/{a}: missing README.md")
    attrs = root / ".gitattributes"
    lf_rule = attrs.is_file() and "*.sh text eol=lf" in read(attrs)
    for p in files(root):
        rel = p.relative_to(root)
        if p.suffix == ".sh" and not lf_rule:
            problems.append(f"{rel}: shell script not covered by '*.sh text eol=lf' in .gitattributes")
        if p.suffix not in TEXT:
            continue
        text = read(p)
        if "\u2014" in text:
            problems.append(f"{rel}: contains an em dash")
        if p.suffix == ".md" and rel.parts[0] != "docs":
            for m in OLD_PATH.finditer(text):
                problems.append(f"{rel}: old path '{m.group(0)}', use advanced/{m.group(1)}")
            for target in link_targets(text):
                base = root if target.startswith("/") else p.parent
                if not (base / target.lstrip("/")).exists():
                    problems.append(f"{rel}: broken link {target}")
    return problems


if __name__ == "__main__":
    found = check(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."))
    print("\n".join(found) if found else "OK")
    sys.exit(1 if found else 0)
