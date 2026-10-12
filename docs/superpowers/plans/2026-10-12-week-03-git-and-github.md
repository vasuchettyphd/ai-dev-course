# Week 3 (Git and GitHub) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish week 3. Students install the GitHub CLI and sign in with it, then use Claude Code to turn `my-first-project` into a git repository. They push it to a private GitHub repository, make a change on a branch through a pull request, and undo a change. The week also includes slides, an assignment, instructor notes and new rows in the instructor's test checklist.

**Architecture:**
- Same approach as week 2.
- Every git, `gh` and Claude Code fact comes from official docs and is recorded on a fact sheet with its URL.
- The local git steps and the `gh` install are run for real in a clean Ubuntu container.
- Steps that need a real GitHub account (`gh auth login`, push, opening and merging a PR, adding a collaborator) carry the "being tested" note and get rows in the instructor's checklist.

**Tech Stack:** Markdown, Marp (`npm run slides` in Docker), Docker `ubuntu:24.04`, git, GitHub CLI.

**Spec:** `docs/superpowers/specs/2026-10-10-course-design.md`, week 3 row. The week 3 design was approved in conversation on 2026-10-12. Decisions: students authenticate with the GitHub CLI; student repositories are **private**, and students add the instructor's GitHub account `vasuchettyphd` as a collaborator.

## Global Constraints

- Audience: business and non-CS students in week 3. They have Claude Code from week 2 and use it to run git. The README explains each concept in plain words and shows each command exactly, labelled with where to type it.
- Students ask Claude Code to do the git work in plain English, so they learn what the commands mean without memorising them. The README shows the prompt to type, what Claude Code will probably do, and what to check afterwards.
- Student repositories are private. The README explains why: business ideas stay private. The assignment asks students to add `vasuchettyphd` as a collaborator.
- Authentication is `gh auth login` with the browser. Students never create, copy or paste personal access tokens.
- Commit email: point students to GitHub's private noreply email setting, so their personal email isn't published.
- Facts come from official sources only, recorded on the fact sheet: git-scm.com, docs.github.com, cli.github.com and GitHub's own install docs, and code.claude.com docs.
- Anything not observed in the dry run is marked "being tested".
- No em dashes (U+2014). The rubric is a table under `## Rubric` with points in the last column, totalling 10.
- Instructor-only material goes in the private repo. Add week 3 rows to `weeks/03-git-and-github/test-checklist.md` there.
- Branch `week-03-git-and-github` in the course repo and `week-03` in the instructor repo. Never commit to main. When asking the user to merge, put the bare PR links first, one per line.

## Review Focus

1. **The student pushes to a public repository by accident.** Every create step says "private", and the troubleshooting section says how to make a repository private.
2. **The wrong GitHub account is signed in.** Show how to check with `gh auth status` and how to switch.
3. **The push is rejected because the remote changed after a merge on GitHub.** Students must pull before pushing again. The README teaches "pull after you merge", and the troubleshooting covers the rejection message.
4. **Students are afraid of losing work.** The undo step must use a safe method: discard uncommitted changes, or revert a commit. Never `reset --hard` on pushed history. Say plainly which one Claude Code should use.
5. **Mac without Homebrew.** The `gh` install path for Mac must not assume Homebrew. Use GitHub's official package installer, or state the prerequisite clearly.

---

### Task 1: Fact sheet and dry run

**Files:** none in the repo. Write the report only.

- [ ] **Step 1: Fact sheet.** Record each fact with its URL:
  - git basics: what a commit, branch and remote are, and `git --version`
  - GitHub account creation and the GitHub Student Developer Pack
  - the commit email privacy setting, and the noreply address format
  - the GitHub CLI install for macOS without Homebrew (official pkg) and for Ubuntu/Debian (official apt repository steps)
  - `gh auth login` interactive choices, and the WSL browser and code behaviour
  - `gh auth status`
  - `gh repo create` with `--private` and pushing from the current folder
  - creating, merging and pulling a PR (the `gh pr create` flags, and merging on the web)
  - adding a collaborator to a private repo
  - making a repo private
  - the git messages for a rejected push and for "not a git repository"
  - how Claude Code handles git (from code.claude.com docs, e.g. the common workflows page)
- [ ] **Step 2: Dry run in a clean `ubuntu:24.04` container**, as a non-root user.
  - Install git if it's missing and record whether it was preinstalled.
  - Install `gh` with the official apt steps, then run `gh --version`.
  - In a new folder:
    - `git init`
    - configure a placeholder name and the noreply-style email
    - commit a file
    - `git log --oneline`
    - create a branch, change and commit
    - `git diff` between branches
    - discard an uncommitted change with `git restore`
    - revert a commit with `git revert`
  - Record the exact output for each.
  - Do not authenticate to GitHub and do not push.
- [ ] **Step 3:** Write the fact sheet, the transcript, the versions and the date to the report.

### Task 2: README, slides and assignment

**Files:** `weeks/03-git-and-github/README.md` (replace the stub, starting from `templates/README.md`), `slides.md`, `slides.pdf`, `assignment.md`.

- [ ] **README:** write it from the Task 1 report and the approved design, in this order:
  1. what git and GitHub are, and why they matter with AI (the undo button)
  2. the GitHub account and private email
  3. check git
  4. install `gh` (Mac and Ubuntu paths)
  5. `gh auth login` and `gh auth status`
  6. make `my-first-project` a repo through Claude Code (example prompts, what to check, the history)
  7. push to a new **private** GitHub repo with `gh`
  8. the branch, PR, merge on GitHub and pull loop
  9. undo safely: discard an uncommitted change, and revert a commit
  10. add `vasuchettyphd` as a collaborator
  11. check it worked
  12. troubleshooting

  Put "being tested" notes on every step that needs a GitHub account. In "Tested with", give the git and `gh` versions and the date, and say exactly what was tested.
- [ ] **Slides:** 16-20 slides, matching the README. Build with `npm run slides`, render to PNG and look at them.
- [ ] **Assignment:**
  - **Hand in:** the private repo URL with `vasuchettyphd` added as a collaborator; the URL of a merged PR; and a short reflection on when they'd use a branch.
  - **Rubric:**
    - The repo exists, is private, and the collaborator is added: 4 points (2 for the repo, 2 for the collaborator)
    - The merged PR, with a sensible title and description: 3 points
    - The reflection: 3 points
    - Total: 10 points
- [ ] **Checks:** `python3 scripts/check_course.py` prints OK. No em dashes. A command-to-source table in the report.

### Task 3: Instructor notes and checklist rows (private repo)

- [ ] `weeks/03-git-and-github/notes.md`, with the four headings:
  - **Timing:** a 75-minute plan.
  - **Common problems:**
    - the wrong account
    - a public repo created by mistake
    - a rejected push
    - the Mac developer tools prompt
    - WSL browser sign-in
    - students who skipped week 2
  - **Discussion answers.**
  - **Grading guidance:** worked 10/10 and 6/10 examples that add up under the rubric. How to find student repos: GitHub sends a collaborator invitation, which the instructor must accept, so include the invitations page URL.
- [ ] `weeks/03-git-and-github/test-checklist.md`: Mac and Windows tables, in the same format as week 2, one row per README step.
- [ ] No em dashes. Commit on `week-03`.

### Task 4: PRs and tracking (controller)

- [ ] Push both branches and open the PRs. Give the user the bare PR links first, one per line.
- [ ] After merge, close the OpenProject task "Week 3: Git and GitHub" in project 4.
