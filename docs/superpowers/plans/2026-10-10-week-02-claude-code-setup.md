# Week 2 (Setting up Claude Code) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 2. Students get Claude Code installed on a Mac, or on Windows via WSL, sign in with Claude Pro, and run a first session. In that session they meet permission prompts and write a CLAUDE.md. The week includes slides, an assignment and instructor notes, plus a test checklist the instructor runs on a real Mac and a real Windows laptop.

**Architecture:**
- The prose follows the course templates and passes `scripts/check_course.py`.
- Every command and product claim is taken from Anthropic's official Claude Code docs. Each one is recorded on a fact sheet with its source URL.
- The Linux/WSL steps are run for real in a clean Ubuntu container, and what the installed version actually shows is recorded.
- The Mac and Windows steps carry a visible "being tested" note until the instructor's checklist comes back.

**Tech Stack:** Markdown, Marp (built with `npm run slides` in Docker), and Docker `ubuntu:24.04` for the dry run.

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`, week 2 row. The week 2 design was approved in conversation on 2026-10-10: Windows students use WSL, and the instructor tests the Mac and Windows steps.

## Global Constraints

- Audience: business and non-CS students in week 2. Week 1 needed nothing installed; this week is their first time in a terminal. Every command is shown exactly, with what they should see. Tone is plain and calm.
- Windows students use WSL 2 with Ubuntu. After installing WSL, every step is identical for Mac and Windows.
- Install with the native installer, `curl -fsSL https://claude.ai/install.sh | bash`, on Mac and inside WSL. No Node.js, no npm and no sudo.
- Every Claude Code command, prompt wording, key and claim must come from the fact sheet (`docs/` URLs under https://code.claude.com/docs/en/). Where the docs and the dry run disagree, describe what the dry run showed, and record the difference.
- Pin the tested Claude Code version and the test date in the README's "Tested with" line.
- Mac and Windows steps are marked: "These steps are being tested on a real Mac / Windows laptop. If something looks different, tell your instructor." The instructor removes the marker after testing.
- Students sign in with their own Claude Pro account. The course never asks for, or stores, passwords or API keys.
- No em dashes (U+2014) in any file. The week 2 rubric is a table under `## Rubric` with points in the last column, totalling 10.
- Instructor-only material, including the test checklist, goes only in the private repo `~/claude/ai-dev-course-instructor`.
- Branch `week-02-claude-code-setup` in the course repo and `week-02` in the instructor repo. Never commit to main. The user merges, and every merge request comes with full PR links.

## Review Focus

1. **The permission lesson doesn't match what students see.** Recent versions may start in a mode that asks fewer questions. Task 1 records the starting mode and the Shift+Tab cycle in the installed version. Task 2's permission section describes exactly that, and tells students how to get to the mode where prompts appear for the exercise.
2. **The WSL browser login fails.** In WSL the sign-in redirect often doesn't come back. The README must cover pressing `c` to copy the link, and the "Paste code here if prompted" step. Task 2's troubleshooting table includes both.
3. **Commands get pasted into the wrong window.** A Windows student runs the Linux install command in PowerShell. Each command is labelled with where to type it ("in PowerShell" or "in the Ubuntu window"), and the troubleshooting table covers the resulting error.
4. **Virtualization is turned off.** `wsl --install` fails on some laptops. The troubleshooting table and the instructor notes say what to do: turn on virtualization in the BIOS or UEFI, and get help in office hours.
5. **Students wonder about cost.** The README says plainly that Claude Pro covers Claude Code and that `/usage` shows how much they've used. It makes no invented limit numbers. Where it mentions limits, it links https://claude.com/pricing.

---

### Task 1: Fact sheet and Linux/WSL dry run

**Files:** none in the repo. The task report holds the fact sheet and the dry-run transcript.

- [ ] **Step 1: Fact sheet.** Fetch these pages and record every fact the week will use, each with its URL:
  - https://code.claude.com/docs/en/setup.md
  - https://code.claude.com/docs/en/quickstart.md
  - https://code.claude.com/docs/en/authentication.md
  - https://code.claude.com/docs/en/troubleshoot-install.md
  - https://code.claude.com/docs/en/permission-modes.md
  - https://code.claude.com/docs/en/permissions.md
  - https://code.claude.com/docs/en/memory.md
  - https://code.claude.com/docs/en/commands.md
  - https://code.claude.com/docs/en/costs.md

  The facts to record:
  - install, verify (`claude --version`, `claude doctor`) and update commands
  - WSL 2 vs WSL 1, and the Exec format error fix
  - the sign-in flow (browser, `c` to copy, paste code, `Login successful`)
  - permission prompt options and the permission modes, with the Shift+Tab cycle and the starting mode
  - CLAUDE.md locations and `/init`
  - `/usage`, `/status`, `/help`, `/clear`, `/exit`, `/login` and `/logout`
  - system requirements

  Also fetch https://learn.microsoft.com/en-us/windows/wsl/install for `wsl --install` and the restart step.
- [ ] **Step 2: Dry run in a clean container.**

  ```bash
  docker run --rm -it ubuntu:24.04 bash -lc 'apt-get update -qq && apt-get install -y -qq curl ca-certificates >/dev/null && useradd -m student && su - student -c "curl -fsSL https://claude.ai/install.sh | bash; export PATH=\$HOME/.local/bin:\$PATH; claude --version; claude doctor || true"'
  ```

  Run it non-interactively where possible; if `-it` is not available, drop it. Record:
  - the exact installer output
  - where it installed and whether PATH needed changing
  - the `claude --version` output
  - the `claude doctor` output

  Then start `claude` in an empty folder, using `script` or `expect` if needed. Capture the first-run screen up to the sign-in prompt, and record its exact wording.

  Do not sign in. Pressing `c` must not be needed.
- [ ] **Step 3: Starting mode.** Use the fact sheet and the version installed, and if possible the CLI's own help (`claude --help`) or settings docs. Record which permission mode a new interactive session starts in, and the Shift+Tab cycle order. If these can't be confirmed without signing in, say so plainly.
- [ ] **Step 4: Report.** Write the fact sheet, the transcript, the version, the date and any doc-vs-reality differences to the task report.

### Task 2: README, slides and assignment

**Files:**
- Modify: `weeks/02-claude-code-setup/README.md` (replace the stub, starting from `templates/README.md`)
- Create: `weeks/02-claude-code-setup/slides.md`, `slides.pdf`, `assignment.md`

**Consumes:** the Task 1 report (fact sheet, transcript, version, starting mode).

- [ ] **Step 1: README.md.** Use the template sections and the Global Constraints. Content in this order:
  1. **What Claude Code is.** It works with files in a folder on your computer and asks before acting, unlike claude.ai chat. It needs Claude Pro; the free plan has no Claude Code.
  2. **Get Claude Pro.** Link to the pricing page and say what the subscription covers.
  3. **Mac path:**
     - open Terminal (Spotlight, "Terminal")
     - run the install command
     - check it with `claude --version`, showing the expected output shape from the dry run
  4. **Windows path:**
     - open PowerShell as administrator and run `wsl --install`
     - restart the computer
     - create the Ubuntu username and password, explaining that typing a password shows nothing
     - in the **Ubuntu** window, run the same install command and check
     - show `explorer.exe .` to open the current folder in File Explorer

     Use the WSL 1 note and the fix from the fact sheet.
  5. **First session.**
     - `mkdir my-first-project && cd my-first-project && claude`
     - sign in, including the WSL copy-link and paste-code steps
     - ask "Create a file called hello.md with three tips for staying organised, then explain what you did"
     - meet a permission prompt: what Yes, "Yes, and don't ask again" and No mean, and when to say No
     - permission modes and Shift+Tab, exactly as Task 1 recorded them
  6. **CLAUDE.md.**
     - what it is and where it lives
     - run `/init`
     - add three personal preferences, for example "Explain things in plain English", "Ask before deleting files" and "Keep answers short"
     - start a new session and see the effect
  7. **Cost and safety:**
     - Pro covers Claude Code; check usage with `/usage`, and link the pricing page for limits
     - never paste passwords, keys or other people's private data
     - read every prompt before saying yes
     - `/exit` to leave
  8. **Check it worked:** `claude --version` works, a session starts, and the student has a CLAUDE.md with three preferences.
  9. **Troubleshooting table:**
     - "command not found" after install: open a new terminal, or follow the PATH fix from the dry run
     - the Linux command run in PowerShell
     - `wsl --install` fails because virtualization is off
     - Exec format error from WSL 1
     - the browser doesn't open in WSL, or the login doesn't come back
     - "Free plan" or no access
     - typing a password shows nothing, which is normal

  Mark the Mac and Windows sections with the "being tested" note. Put the version and date in "Tested with". Remove the stub marker.
- [ ] **Step 2: slides.md, then the PDF.** Write 16-20 slides:
  - title and agenda
  - what Claude Code is
  - what it costs
  - the two install paths
  - live demo cues: install, first session and a permission prompt
  - permission modes
  - CLAUDE.md
  - safety
  - the assignment
  - next week (git)

  Build with `npm run slides`, render the slides to PNG in the scratchpad and look at them.
- [ ] **Step 3: assignment.md.**
  - **What to do:** take a screenshot of `claude --version`, take a screenshot of the first session with a permission prompt, and write their CLAUDE.md with three preferences. Write one short paragraph: which prompt they saw, what they chose, and why.
  - **Hand in:** one document.
  - **Rubric:**
    - Claude Code installed and running, with the screenshots: 4 points
    - CLAUDE.md with three meaningful preferences: 3 points
    - The permission reflection shows they understood what they approved: 3 points
    - Total: 10 points
- [ ] **Step 4: Checks.** `python3 scripts/check_course.py` prints OK. There are no em dashes. Every command in the README matches the fact sheet or the transcript; list each command in the report next to its source.

### Task 3: Instructor notes and the test checklist (private repo)

**Files (instructor repo, branch `week-02`):**
- Modify: `weeks/02-claude-code-setup/notes.md`
- Create: `weeks/02-claude-code-setup/test-checklist.md`

- [ ] **notes.md**, with the four headings:
  - **Timing:** a 75-minute plan. Allow for the WSL restart: suggest Windows students run `wsl --install` before class.
  - **Common problems:** virtualization off; work laptops that block admin rights or WSL; Chromebooks and old Windows versions that can't run it (from the system requirements); the free plan; the WSL login redirect; Exec format error; the PATH issue.
  - **Discussion answers.**
  - **Grading guidance:** worked 10/10 and 6/10 examples that add up under the rubric.
- [ ] **test-checklist.md:** one checklist for a Mac and one for a Windows laptop. Every README step gets a numbered line with what the tester should see, taken from the README and transcript, plus "what you saw / OK?" columns. Finish with "send the results to Claude to update the README and remove the 'being tested' notes".
- [ ] No em dashes. Commit on `week-02`.

### Task 4: PRs and tracking (controller)

- [ ] Push both branches and open the PRs. Give the user the **full PR links** and ask them to squash-merge.
- [ ] Create and close the OpenProject task "Week 2: Setting up Claude Code" in project 4.
- [ ] Tell the user to run `test-checklist.md` on a Mac and a Windows laptop, and that the "being tested" notes come out once they report back.
