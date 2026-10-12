# Week 7: Running what you build

**Goal:** put your project in a Docker **container**, so it runs the same way on any laptop with Docker: install Docker Desktop, have Claude write a `Dockerfile` and `.dockerignore` for your project, run your program and its tests inside the container, check the files with your week 6 `safe-and-private` reviewer, and merge them through a pull request.

**Time:** plan for about 2 hours of your own time (an estimate), **plus installing Docker Desktop before class** (step 2). **Cost:** nothing beyond your Claude plan. Docker Desktop is free for personal use and education (step 2a).

> **Do step 2 before class.** Installing Docker Desktop is the step most likely to need help (especially on Windows). Do it early in the week, so there's time for office hours if it doesn't work.

**Tested with** (12 October 2026; these are the versions tested, yours may be newer):

- Docker Engine 29.8.0 (build 88096ef) on Linux (WSL 2, Intel/AMD chip), **not** Docker Desktop.
- The official `python:3.12-slim` image, which was Python 3.12.15 that day.
- The deal screener example in a container: its 39 tests passed; listing B gave the same answer as outside the container, character for character; without `-it` it stopped with `Stopped before all the numbers were typed.`; the image was about 180 MB (177 MB on Docker Engine; the number Docker Desktop shows is being tested).
- `docker run hello-world`, `docker build`, `docker run --rm`, `docker image ls` and the `docker image prune` question.
- The instructor ran the `safe-and-private` reviewer on the deal screener's `Dockerfile` and `.dockerignore`. The result is the "Week 7" section of [`example-project/REVIEW.md`](../../example-project/REVIEW.md).
- Being tested on real Mac and Windows laptops: installing and running Docker Desktop (Mac with an Apple chip, Intel Mac, Windows with WSL 2), its screens, prompts and settings, Windows Home, typing into a program in a container in a real terminal, everything inside a signed-in Claude Code session, and everything on GitHub. These follow Docker's official docs, linked in each step.

## Before you start

You need:

- Weeks 5 and 6 done: your build and your review fixes merged into `main` of your **private** `semester-project` repo, with `vasuchettyphd` as a collaborator, and the tests passing.
- Your week 6 reviewers in `.claude/agents/` (this week uses `safe-and-private`).
- Your hand-worked example from week 5 (step 4d), and the command that runs your tests (for example `python3 -m unittest` or `npm test`).
- The course repo on your laptop, in `~/ai-dev-course` (week 6 step 3b).
- `gh` signed in to **your** GitHub account (`gh auth status` shows your username), and Claude Code signed in with your Claude Pro account.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows, as in weeks 2 to 6. Every command below says where to type it: **in your terminal**, **in Claude Code** (the `claude` session), or, for a few Windows install checks only, **in PowerShell**. **In a second terminal window** means a new window, so Claude Code keeps running in the first one (week 5 shows how).

### How you'll work this week

As in weeks 5 and 6, you ask Claude Code in plain English. For each step this README shows **the prompt** to type, **what Claude Code will probably do** (its exact words will differ), and **what to check** afterwards.

The rules from weeks 5 and 6 still apply:

- Make the branch first (step 3a), before Claude writes anything. Never change `main`.
- For **git** commands, always pick plain **Yes**, never "Yes, and don't ask again" or "Yes, and switch to auto mode".
- Finish with a push and a pull request, read **Files changed**, merge on GitHub, then pull.

What to answer this week:

| Claude asks to | Choose |
|---|---|
| Create or edit `Dockerfile`, `.dockerignore`, `README.md` or `REVIEW.md` | **Yes** |
| Read-only commands: `git status`, `git log`, `git diff`, `ls`, `docker image ls` | **Yes** |
| `git add`, `git commit`, `git push` on `containerize`, `gh pr create` | plain **Yes** |
| `docker build -t semester-project .` or `docker run --rm semester-project ...` | **Yes** |
| `docker system prune -a` | **No**: it deletes every image not in use, not only this project's |
| Anything with `--privileged` | **No**: it switches off the container's safety limits, and nothing this week needs it |
| Anything that mounts your home folder into a container (`-v ~:...`, `-v $HOME:...`, or `--mount` naming your home folder) | **No**: the container could then read and change all your files |
| A `FROM` line that ends in `:latest`, or has no version at all (such as `FROM python`) | **No**: ask for a pinned version (step 3b) |
| `docker login` or `docker push` | **No**: your image stays on your laptop |
| Anything that changes `main`, or `reset --hard`, `--force`, `git clean`, `rm -rf` | **No** |

After a No, tell Claude why, for example: "Don't use --privileged. Find another way, and explain it first."

## Steps

### 1. Why containers

**"It works on my machine."** You finish your project, it passes every test, and you send it to a classmate. On their laptop it fails: they have a different version of Python, or no Python at all, or a package your project needs is missing. Nothing is wrong with your code. What's different is everything around it. Programmers have a name for this problem: "works on my machine".

A **container** packs your program together with everything around it that it needs: the language (Python 3.12, say), the packages, and your files. Docker then runs that package the same way on a Mac with an Apple chip, an Intel Mac and Windows. Inside, it's always a small Linux computer, whichever laptop it runs on.

**Image and container: a recipe and a dish.**

| Docker word | In the kitchen | What it is |
|---|---|---|
| `Dockerfile` | The recipe card you write | A short text file: start from this base, add these files, run this command |
| **Image** | The recipe, with every ingredient measured and packed | What `docker build` makes from the `Dockerfile`. It sits on your laptop and doesn't change |
| **Container** | A dish cooked from the recipe | What `docker run` starts from an image. Cook as many as you like, each the same; when you've eaten, the plate is cleared (`--rm`) |
| `.dockerignore` | What stays out of the kitchen | A list of files Docker must **not** pack: secrets, git's history, big add-on folders |

You build the image once, then run a container from it whenever you want to use the program. The deal screener's `Dockerfile`, [`example-project/Dockerfile`](../../example-project/Dockerfile), has five lines, each with a plain-English note above it:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
USER nobody
CMD ["python", "-m", "dealscreener"]
```

1. `FROM python:3.12-slim`: start from Docker's **official** Python image. `3.12` keeps Python on version 3.12 (it still gets small fixes); `slim` leaves out extras the program doesn't use. Never `latest`, which can change under you. (Docker's Python page doesn't use the word "pin"; this course calls a fixed version like `3.12` a **pinned** version. The course uses `python:3.12-slim` everywhere.)
2. `WORKDIR /app`: work in a folder called `/app` inside the container.
3. `COPY . .`: copy this folder into `/app`, leaving out everything in `.dockerignore`.
4. `USER nobody`: run as `nobody`, a user with no special powers. This line is optional (step 3b).
5. `CMD [...]`: the command that runs when the container starts.

The deal screener needs no packages, so it has no install line. Its `Dockerfile` notes say where one would go.

### 2. Install Docker Desktop (before class)

> **Being tested:** Everything in this step comes from Docker's install pages, linked below, and is being tested on real laptops. Screens, buttons and prompts may look a little different.

You install **Docker Desktop**, Docker's app for Mac and Windows. Follow the path for your laptop: **2b** (Mac with an Apple chip), **2c** (Intel Mac) or **2d** (Windows). Then everyone does **2e**.

**a. Before you install, on any laptop.**

- **Licence.** Docker Desktop is free for "Personal use", "Education", "Small businesses (fewer than 250 employees AND less than $10 million in annual revenue)" and "Non-commercial open source projects" (<https://docs.docker.com/subscription/desktop-license/>). Your course work is personal use and education. If your laptop belongs to an employer bigger than that, ask your employer before installing it.
- **Admin rights.** On a Mac, Docker's page says "No further configuration is needed and you aren't asked for a password." On Windows, the installer's per-user mode "needs no administrator privileges". If your laptop is managed by a school or employer and blocks installs, ask your instructor before class.
- **Disk space.** Docker's pages don't give a number. The deal screener's image was about 180 MB in our test, and yours will likely be about that size, or more if your project installs packages. If your laptop is nearly full, free some space first.
- **Keep it running.** `docker` commands only work while Docker Desktop is open and running. If you quit it, start it again before you type a `docker` command.

**b. Mac with an Apple chip.** Check your chip first, as in [week 3](../03-git-and-github/) step 3: Apple menu > **About This Mac**. **Chip** followed by a name such as `Apple M1` means an Apple chip. **Processor** followed by an **Intel** name means an Intel Mac: go to 2c.

Docker's Mac page is <https://docs.docker.com/desktop/setup/install/mac-install/>. Its requirements: "Docker Desktop is supported on the current and two previous major macOS releases" (the page gives no version numbers; About This Mac shows yours), and "At least 4 GB of RAM" (About This Mac shows **Memory**).

1. On that page, download **Docker Desktop for Mac with Apple silicon**.
2. In **Downloads**, double-click `Docker.dmg`, then drag the Docker icon to the **Applications** folder.
3. In **Applications**, double-click `Docker.app` to start Docker.
4. It shows the **Docker Subscription Service Agreement**. Read it and accept: "Docker Desktop won't run if you do not agree to the terms."
5. Docker's page says Rosetta 2 (Apple's tool for running Intel programs) is recommended on Apple chip Macs, but "no longer strictly required". If Docker Desktop or macOS offers to install it, say yes (being tested).
6. If macOS asks whether to open an app downloaded from the internet, or to allow something for Docker, allow it (being tested).

Then do 2e.

**c. Intel Mac.** The same as 2b, with the other download. On <https://docs.docker.com/desktop/setup/install/mac-install/>, download **Docker Desktop for Mac with Intel chip**. Then do steps 2 to 4 and 6 of 2b (Rosetta is only for Apple chips), and then 2e.

**d. Windows (WSL 2).** You set up WSL 2 and Ubuntu in week 2. Docker Desktop for Windows runs on WSL 2 and gives your Ubuntu window the `docker` command. Docker's Windows page is <https://docs.docker.com/desktop/setup/install/windows-install/>.

1. **Check your Windows.** Press `Win + R`, type `winver` and press Enter (as in week 2). Docker's requirements:
   - "Windows 10 64-bit: Enterprise, Pro, or Education version 22H2 (build 19045)", or
   - "Windows 11 64-bit: Enterprise, Pro, or Education version 23H2 (build 22631) or higher".
   - "8GB system RAM", "WSL version 2.1.5 or later", and "Enable hardware virtualization in BIOS/UEFI" (you needed virtualization for WSL in week 2 too).

   To see your **edition**, open **Settings > System > About** and look at **Edition** (being tested). Docker's list names Enterprise, Pro and Education, **not Home**; elsewhere the page says "Windows Home or Education editions only allow you to run Linux containers". Docker's page does not list Home as supported, so Home is being tested. **If yours says Home, ask your instructor before you install.**
2. **Check WSL** (being tested). In **PowerShell** (Start, type `PowerShell`, open **Windows PowerShell**), type:

   ```powershell
   wsl --version
   ```

   The first line shows the WSL version; it must be 2.1.5 or later. If it's older, or `wsl --version` isn't recognised, type `wsl --update` and try again. Then type `wsl.exe -l -v`: your `Ubuntu` must show VERSION `2` (if it shows `1`, type `wsl --set-version Ubuntu 2` in PowerShell, as in week 2's Troubleshooting row for `Exec format error`).
3. **Download and install.** On Docker's Windows page, download Docker Desktop for Windows with the download button on that page (the x86_64 one, for the Intel and AMD chips most Windows laptops have; if your laptop has an Arm chip such as Snapdragon, ask your instructor first; being tested). In **Downloads**, double-click `Docker Desktop Installer.exe`.
   - If it asks how to install, choose **per-user**: Docker's page says "Per-user is recommended and needs no administrator privileges".
   - On the **Configuration** page, make sure **Use WSL 2 instead of Hyper-V** is selected.
   - Follow the steps, then click **Close**.
4. **Start it.** Docker Desktop doesn't start by itself after installing. Click Start, search for **Docker** and choose **Docker Desktop**.
5. It shows the **Docker Subscription Service Agreement**. Read it and select **Accept**: Docker Desktop won't run otherwise.
6. **Check Ubuntu is connected.** In Docker Desktop, go to **Settings > Resources > WSL Integration**. Docker's page says integration is on by default for your default WSL distribution, which is Ubuntu. Check that **Ubuntu** is switched on there (the exact label is being tested); if you changed anything, click **Apply**. While you're in Settings, **General** should have **Use WSL 2 based engine** ticked (being tested).

   - If **WSL Integration** isn't under **Resources**, Docker's page says Docker "may be in Windows container mode": right-click the Docker icon in the taskbar and choose **Switch to Linux containers** (being tested).
   - If Ubuntu isn't your default, type `wsl.exe --set-default Ubuntu` in PowerShell (being tested), then restart Docker Desktop.

From here on, every `docker` command goes in the **Ubuntu window**, never in PowerShell. Then do 2e.

**e. Check it works (everyone).** With Docker Desktop running, in your terminal (Terminal on a Mac, the **Ubuntu window** on Windows), type:

```bash
docker --version
```

It prints a version, such as `Docker version 29.8.0, build 88096ef` in our test (yours will probably differ). Then type:

```bash
docker run hello-world
```

The first time, it downloads a tiny test image, so it starts with lines like these:

```text
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Status: Downloaded newer image for hello-world:latest
```

then a blank line, then **`Hello from Docker!`** and "This message shows that your installation appears to be working correctly." That's the line to look for. (`hello-world` uses `latest`, which is fine for a one-off test; your own `Dockerfile` never does.) An error instead? See Troubleshooting.

### 3. Containerize your project

> **Being tested:** This step needs a signed-in session and is being tested. The deal screener's two files were tested for real.

**a. Start Claude Code and make the branch, before Claude writes anything.** In your terminal:

```bash
cd ~/semester-project && claude
```

Press `Shift + Tab` until the bottom line says `manual mode on`. Then, in Claude Code:

```text
Show me git status.
```

It should say `nothing to commit, working tree clean`. If it lists files, don't go on: ask "What are these files, and where did they come from? Don't change anything.", and ask in office hours if you're not sure. When it's clean, type:

```text
Switch to main and pull the latest changes from GitHub. Then make a new branch called containerize and switch to it.
```

It will probably run `git switch main`, `git pull` and `git switch -c containerize`. Plain **Yes**. Check: ask "What branch am I on?". It should say `containerize`. (If that name is taken, use `containerize-2`, here and everywhere this README says `containerize`.)

**b. Copy the deal screener's two files as a starting point.** As in week 6 step 3b, you copy them yourself, in a **second terminal window**. First update the course repo, then copy:

```bash
cd ~/ai-dev-course && git pull
cd ~/semester-project
cp ~/ai-dev-course/example-project/Dockerfile ~/ai-dev-course/example-project/.dockerignore .
ls -a
```

`ls -a` should now list `Dockerfile` and `.dockerignore` among your files (`ls` alone hides names starting with a dot). If `cp` says `cannot stat`, the course repo is older than week 7 or in another folder: run `git pull` in it and check the path.

**c. Make them fit your project.** The copied `Dockerfile` runs the deal screener, not your program. In Claude Code (the first window), type:

```text
I copied Dockerfile and .dockerignore from a Python project, a rental deal screener, as a model. Read them, then read PLAN.md, README.md and my code, and adapt both files to my project. Rules: start from an official image on Docker Hub for my language, pinned to a version, never latest (if my project is Python, use python:3.12-slim, as the model does), and a slim version if there is one. If my project needs packages, copy its package list and install them before COPY . ., as the model's comment says. The last line must start my program the way my README says. Never copy a .env file, passwords, keys or other secrets into the image, and keep .dockerignore leaving out .git, .venv, venv, node_modules, __pycache__ and .env files, with the **/ patterns the model uses, plus .claude, .superpowers, docs and REVIEW.md. If my program reads data files (such as CSV or JSON), tell me which ones and keep only those in the image, without copying anything private. Keep USER nobody unless my program writes files inside the container; if it does, tell me. Don't add --privileged, ports or folders from my laptop. Keep a plain-English comment above every line. Don't build or run anything yet, and don't commit. Show me both files when you're done.
```

**What Claude Code will probably do:** read your files, then ask to edit `Dockerfile` and `.dockerignore` (plain **Yes**), and show them. Check the `FROM` line: it names an official image with a version, such as `python:3.12-slim`, and no `latest`. If anything in the table under "How you'll work this week" says **No**, answer No. The model `.dockerignore` leaves out every CSV file (`**/*.csv`) because the deal screener reads none; if your program needs a data file, Claude should keep that one in.

**d. Read the Dockerfile.** You don't need to write Dockerfiles, but you should know what yours does. In Claude Code:

```text
Explain each line of the Dockerfile in plain English.
```

Compare with the five lines in step 1. If a line is there that you don't follow, ask about that line until you do. Things to check:

- `FROM` names an official image and a version, not `latest`.
- Nothing copies a `.env` file or a secret on purpose.
- The last line (`CMD`) runs your program, not the deal screener.

### 4. Build and run

> **Being tested:** The commands, and the deal screener's output below, were tested on Docker Engine 29.8.0. Docker Desktop on a Mac or Windows, and your own project, are being tested.

Type these **yourself**, in your **second terminal window** (`cd ~/semester-project` first), with Docker Desktop running. To open one: on a Mac, click Terminal and press `Cmd + N`; on Windows, open **Ubuntu** again from the Start menu (don't type `wsl` in PowerShell). You see the output directly, and you can type into your program.

**a. Build the image.**

```bash
docker build -t semester-project .
```

`-t semester-project` names the image `semester-project`; the final `.` means "this folder" (Docker looks for the `Dockerfile` there). The first build downloads the official base image, so it takes longer; later builds are quick. It prints numbered steps such as `[1/3] FROM docker.io/library/python:3.12-slim` and ends with a line like `naming to docker.io/library/semester-project:latest done`. That `latest` is the label Docker gives **your own** image when you don't give one; it's fine. The "never latest" rule is about the `FROM` line.

Build failed? Copy the last 20 lines into Claude Code and see Troubleshooting.

**b. Run your program.**

```bash
docker run -it --rm semester-project
```

- `-it` lets you type into the program: `-i` keeps your typing connected to it, `-t` makes it act like a terminal. If you leave it out, a program that asks questions can't read what you type. The deal screener then prints `Stopped before all the numbers were typed.` and stops.
- `--rm` deletes the container when the program ends, so stopped containers don't pile up. The image stays, so you can run it again.

If your program isn't something you type into (for example a web page), ask Claude how to start it in the container before you run it.

Type in your **hand-worked example from week 5** and compare the answer with yours. It should match, as it did outside the container (to the cent, for money). Take a **screenshot** of the answer with your hand-worked answer beside it: the assignment asks for it. For the deal screener, listing B (price 150000, rent 1700, tax 2400, insurance 1200, HOA 0, down payment 25, interest rate 7, loan term 30, closing costs 6000) gives in the container the same answer as outside it:

```text
Monthly mortgage payment: $748.47
Monthly cash flow: $430.53
Cap rate: 9.43%
Cash-on-cash return: 11.88%

PASS  Cash-on-cash return 11.88% is at least 10.00%
PASS  Monthly cash flow $430.53 is at least $100.00

Overall: PASS
```

Different answer? See Troubleshooting.

**c. Run your tests in the container.** The test command depends on your language, so ask. In Claude Code:

```text
What single command runs my tests inside the semester-project image? It should start with docker run --rm semester-project. Don't run it; just show it to me.
```

For a Python project using `unittest`, it's `docker run --rm semester-project python -m unittest`; for Node.js, it may be `docker run --rm semester-project npm test` (being tested). Type it in your second terminal window. For the deal screener (its image is called `dealscreener`), `docker run --rm dealscreener python -m unittest` printed:

```text
.......................................
----------------------------------------------------------------------
Ran 39 tests in 0.002s

OK
```

Yours will show your own number of tests, in your language's words. Take a **screenshot**: the assignment asks for it.

**d. Check what's inside.** In your second terminal window:

```bash
docker run --rm semester-project ls -a
```

This lists the files in the container's working folder (`/app` in the deal screener's `Dockerfile`). It shows the top folder only, not the folders inside it. For the deal screener:

```text
.
..
.dockerignore
Dockerfile
PLAN.md
README.md
dealscreener
tests
```

Check there's **no** `.env`, `.git`, `.venv`, `venv`, `.claude` or `__pycache__`. (`node_modules` is fine **only** if your `Dockerfile` installs packages itself, inside the image.) Anything that shouldn't be there? See Troubleshooting. To also look inside every folder (optional; tested on the deal screener only, being tested for other projects), type:

```bash
docker run --rm semester-project find . -name ".env*" -o -name ".git" -o -name ".venv"
```

It should print nothing.

To see the image's size, type `docker image ls semester-project` (its columns vary between Docker versions).

**e. Commit.** When the program, the tests and the `ls -a` check are all right, in Claude Code:

```text
Commit Dockerfile and .dockerignore on this branch with the message "Run the project in Docker".
```

Plain **Yes** to `git add` and `git commit`.

### 5. Review it with `safe-and-private`

> **Being tested:** The deal screener's Dockerfile review was run with these reviewer instructions on 12 October 2026. Running this prompt in a signed-in session is being tested.

A `Dockerfile` decides what goes into an image, so it's exactly what your week 6 `safe-and-private` reviewer is for. This time you run only that one reviewer, on the two new files.

**a. Run the review.** In Claude Code:

```text
Run the safe-and-private reviewer as a subagent on Dockerfile and .dockerignore only. Then add a new section at the end of REVIEW.md, headed "## Week 7: Dockerfile review", with one table with the columns #, Label, Finding (file:line), Found by, Decision, Reason. Number the findings D1, D2 and so on, so they don't clash with week 6's numbers. Sort the rows: Must fix first, then Should fix, then Nice to have. Keep each finding's wording close to what the reviewer wrote, and keep its file and line numbers. Leave Decision and Reason empty. Do not add any finding the reviewer did not report, and do not change any file except REVIEW.md. After the table, list in a few words the areas where the reviewer said "Nothing found".
```

Answer as in week 6 step 4c: **Yes** to editing `REVIEW.md`, **No** to editing any other file. After a No, type: "Don't change any file except REVIEW.md." Then read the new section and commit it:

```text
Commit REVIEW.md on this branch with the message "Review of the Dockerfile".
```

**b. Triage, as in week 6 step 5.** Check each finding against the files before you decide ("Check finding D1 in REVIEW.md against the files. Is it right, and are the file and line numbers right? Explain in plain English. Don't change any file."). Then give each one a **Decision** (`Fix` or `Won't fix`) and a **Reason** of one plain sentence. Every Must fix is `Fix`, unless the finding is wrong. The deal screener's reviewer found four things, all Nice to have. Two of its rows (shortened):

| # | Label | Finding | Decision | Reason |
|---|---|---|---|---|
| D2 | Nice to have | `.venv` and `venv` in `.dockerignore` match only at the top folder | Fix | Correct: a bare name only matches at the top folder, so these now use `**/` |
| D3 | Nice to have | The `FROM` line uses a tag, not a digest, so the image can change on rebuild | Won't fix | A digest freezes the image exactly, so it stops security fixes arriving; `3.12-slim` is the course's pin |

Record your decisions (edit `REVIEW.md` yourself, or tell Claude exactly what to write, one finding at a time), then commit. In Claude Code:

```text
Commit REVIEW.md on this branch with the message "Triage the Dockerfile review".
```

**c. Fix, one finding at a time.** In Claude Code, with the finding's number and a few words about it:

```text
Fix finding D1 in REVIEW.md. Change only Dockerfile or .dockerignore, and nothing else. Then commit on this branch with the message "Fix review D1: <a few words>".
```

After each fix, **build and check again** in your second terminal window: `docker build -t semester-project .`, then your test command from step 4c, then `docker run --rm semester-project ls -a`. A fix must not break the build or the tests.

No findings at all? Write that in your reflection; there's nothing to fix.

### 6. Finish

> **Being tested:** This step needs a signed-in session and a real GitHub account, and is being tested.

**a. Tell readers how to run it.** In Claude Code:

```text
Add a short section called "How to run with Docker" to README.md. Say that Docker Desktop must be installed and running, then show three commands, each with one plain sentence on what it does: docker build -t semester-project . to build the image, the test command we used, and docker run -it --rm semester-project to run the program. Say they are typed in Terminal on a Mac or the Ubuntu window on Windows, in the project folder. Change nothing else. Then commit README.md on this branch with the message "How to run with Docker".
```

Plain **Yes** to the edit and the commit. The deal screener's version is the "How to run with Docker" section of [`example-project/README.md`](../../example-project/README.md#how-to-run-with-docker).

**b. Push and open a pull request.** In Claude Code:

```text
Push the containerize branch to GitHub and open a pull request into main titled "Run in Docker".
```

It will probably run `git push -u origin containerize` and `gh pr create ...`. Plain **Yes** to each. It prints the pull request's address. Copy it: you hand it in.

**c. Read Files changed yourself, before you merge.** Open the address and click **Files changed** (week 6 step 2). You should see `Dockerfile`, `.dockerignore`, `README.md`, and `REVIEW.md` (if step 5 updated it), plus any file a step 5 fix changed: nothing else. In particular, no `.env` file and no folder such as `.venv` or `node_modules`. Read the `Dockerfile` once more: an official image with a version on the `FROM` line. If something is there that shouldn't be, don't merge: ask Claude what it is and why.

**d. Merge on GitHub, then pull.** On the **Conversation** tab click **Merge pull request** and **Confirm merge** (or **Squash and merge**; the exact labels are being tested), as in [week 3](../03-git-and-github/) step 7. Then, in Claude Code:

```text
Switch back to main and pull the latest changes from GitHub.
```

Check: ask "What branch am I on, and is the Dockerfile in this folder?". It should say `main`, and yes. Keep your local `containerize` branch until your assignment is graded.

The deal screener's week 7 changes are on this page (it works once week 7 is published): <https://github.com/vasuchettyphd/ai-dev-course/compare/week-06...week-07>.

**e. Tidy up (optional).** Each build can leave old, unnamed copies of your image behind. To see your images, type `docker image ls` in your terminal. To delete only the unused leftovers, type this **yourself**:

```bash
docker image prune
```

It asks `WARNING! This will remove all dangling images.` and `Are you sure you want to continue? [y/N]`. "Dangling" images are the old, unnamed leftovers. Type `y` and press Enter to delete them, or just Enter to stop. Never `docker system prune -a`: it deletes every image not in use, and you'd download them all again.

### 7. Check it worked

You're done when:

- Your pull request's page on GitHub shows it was merged, and **Files changed** shows `Dockerfile`, `.dockerignore`, `README.md` and (if updated) `REVIEW.md`, and no `.env` or tool folders.
- The `FROM` line names an official image with a pinned version, never `latest`.
- On `main`, `docker build -t semester-project .` works, your tests pass in the container, and your program in the container matches your hand-worked example.
- `docker run --rm semester-project ls -a` shows no `.env`, `.git`, `.venv` or `__pycache__`.
- Every finding in the "Week 7: Dockerfile review" section of `REVIEW.md` has a Decision and a Reason.

The [assignment](assignment.md) asks for the pull request's address, two screenshots and a short reflection.

## Troubleshooting

| What you see | What to do |
|---|---|
| (being tested) `Cannot connect to the Docker daemon ...` or a similar "is the docker daemon running?" message | Most likely Docker Desktop isn't running. Start it (Mac: **Applications > Docker**; Windows: Start, search **Docker**, choose **Docker Desktop**), wait until Docker Desktop says it is running, then type the command again. |
| (being tested) `docker: command not found` in the Ubuntu window | Most likely Ubuntu isn't connected to Docker Desktop. Check Docker Desktop is running, then **Settings > Resources > WSL Integration**: switch **Ubuntu** on, click **Apply**, close the Ubuntu window and open a new one (step 2d.6). No **WSL Integration** there? Right-click the Docker icon in the taskbar and choose **Switch to Linux containers**. |
| The line you typed on starts with `PS C:\` | You're in PowerShell. Open **Ubuntu** from the Start menu and type the `docker` command there. PowerShell is only for the WSL checks in step 2d. |
| `Docker Desktop - Unexpected WSL error`, with a code such as `HCS_E_HYPERV_NOT_INSTALLED` or `ERROR_NOT_SUPPORTED` | Virtualization is most likely turned off. Docker's troubleshooting page, <https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/>, says to check the **Performance** tab in Task Manager, and to turn it on in your laptop's BIOS or UEFI settings. That's the same fix as week 2's `wsl --install` row; come to office hours and we'll do it together. |
| `Docker Desktop - Access Denied` (Windows) | Docker's troubleshooting page says your user isn't in the `docker-users` group. That needs an administrator: come to office hours, or ask whoever manages your laptop. |
| Docker Desktop won't start until you accept something | Accept the **Docker Subscription Service Agreement** (step 2): "Docker Desktop won't run if you do not agree to the terms." |
| Your Windows edition is **Home** | Ask your instructor before installing (step 2d.1). Home is being tested. |
| (being tested) `no space left on device`, or your disk is nearly full | In your terminal: `docker image ls` to see your images, then `docker image prune` (step 6e) to delete unused leftovers. Delete any test image you don't need with `docker image rm <name>` (as in our test). **No** to `docker system prune -a`. |
| The build stops at an install line (an error from `pip`, `npm` or `apt-get`) | Copy the last 20 lines into Claude Code: "My docker build failed with this error: <paste>. Explain it in plain English, then fix the Dockerfile. Keep an official image with a pinned version, never latest, and don't change my code." Then build again. |
| (being tested) `failed to read dockerfile` or `no such file or directory` when you build | You're not in your project folder, or the `Dockerfile` isn't there. `cd ~/semester-project`, check `ls` shows `Dockerfile`, and build again. |
| `Stopped before all the numbers were typed.`, or your own program stops with an "end of file" error such as Python's `EOFError` (being tested) | You left out `-it`, so the program couldn't read your typing. Use `docker run -it --rm semester-project`. |
| (being tested) The program waits and nothing happens | It may be waiting for you to type. If you typed `docker run` without `-it`, press `Ctrl + C` and use `docker run -it --rm semester-project`. If it still seems stuck, press `Ctrl + C` and ask Claude: "My program waits forever in the container. Explain why in plain English." |
| (being tested) `exec format error`, or `no matching manifest` with `arm64` or `amd64` in the message | Something in the image was made for another kind of chip. The official `python` image page lists both kinds (`amd64` for Intel and AMD, `arm64v8` for Apple chips; each tag is being tested), so it's usually a package or a non-official image. Ask Claude: "This error mentions my chip: <paste>. I'm on [a Mac with an Apple chip / an Intel Mac / Windows]. Use only official images and package versions made for my chip, and explain the change first." |
| (being tested) The program can't find a file in the container (for example `No such file or directory` or `FileNotFoundError`) | `.dockerignore` probably left it out. Ask Claude: "My program can't find <file> in the container. Which files does it need? Change .dockerignore so only those go in, without copying anything private." Then build again. |
| `Permission denied` when your program saves a file | The `USER nobody` line stops writing inside `/app`. Remove that line from the `Dockerfile`, or ask Claude: "My program gets Permission denied when it saves a file in the container. Fix the Dockerfile, and explain the change." Then build again. |
| `ls -a` (step 4d) shows `.env`, `.git`, `.venv`, `venv`, `.claude` or `__pycache__` | Don't commit or push yet. In Claude Code: "The image contains <name>. Add it to .dockerignore with a **/ pattern, and change nothing else." Build again and check `ls -a` again. If it was a `.env` file, also ask "Is .env in git? Don't change anything." and tell your instructor if it is. |
| The program in the container gives a different answer from your hand-worked example | Check your hand working first. Then tell Claude: "For this input [your input], I worked out [your answer] by hand, but the container says [its answer], and outside the container it says [answer]. Find out why before changing anything." |
| `fatal: a branch named 'containerize' already exists` | Use `containerize-2` instead (step 3a), here and everywhere this README says `containerize`. |
| It committed to `main` | Say **No** to any push of `main`, and to `reset --hard` or `--force`. Then follow [week 5's "If it committed to `main`"](../05-building-with-ai/README.md#if-it-committed-to-main), using `rescue-containerize` as the branch name. |
