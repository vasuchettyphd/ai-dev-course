# Week 7 assignment: Running what you build

## What to do

Follow the [week 7 README](README.md) on your own laptop, in your private `semester-project` repo, then collect four things.

**(a) Your merged pull request.** The address of the merged pull request on `semester-project` from your `containerize` branch (README steps 3 to 6). Its **Files changed** must show:

- your `Dockerfile`, whose `FROM` line names an official image with a pinned version (such as `python:3.12-slim`), never `latest`, and whose last line runs your program;
- your `.dockerignore`, leaving out at least `.git`, `.venv`, `venv`, `node_modules`, `__pycache__` and `.env` files;
- the "How to run with Docker" section in your `README.md`;
- the "Week 7: Dockerfile review" section in `REVIEW.md`, with a Decision and a Reason for every finding (if the reviewer found anything), and any fixes.

No `.env` file, password, key or other secret may be in the pull request or copied into the image. The repo stays **private**, with `vasuchettyphd` as a collaborator, so your instructor can open it.

**(b) A screenshot of your tests passing in the container.** Your terminal after you ran your test command with `docker run --rm semester-project ...` (README step 4c), showing the command and the result.

**(c) A screenshot of your program running in the container on your own example.** Your terminal after `docker run -it --rm semester-project` with your week 5 hand-worked example typed in, or the run command from README step 4b with your example as input, or, for a web page, a screenshot of the page in your browser with your example entered. It shows the program's answer, and your hand-worked answer beside it (a photo of your working, or the numbers typed next to it). Say in one sentence whether they match.

**(d) A short reflection,** about half a page:

1. **What the container made you notice:** one thing about your project you noticed while putting it in a container, for example a package you didn't know it needed, a file that nearly went into the image, or what your program does when it can't read your typing (no `-it`).
2. **The review:** what `safe-and-private` said about your `Dockerfile` and `.dockerignore`, and what you did about it (quote one finding and its Decision). If it found nothing, say which areas it checked and whether you agree, and why.

Never put a password, a sign-in code or a token in your hand-in.

## What to hand in

- One document with the pull request's address, the two screenshots and your reflection.

Submit it the way your course site says.

## Rubric

| Criterion | Points |
|---|---|
| `Dockerfile` and `.dockerignore` merged by pull request: an official base image with a pinned version (no `latest`), the program as the last line, and nothing secret or unneeded copied in | 4 |
| Tests and program run in the container: the tests screenshot (1 point), and the program screenshot on your own example with your hand-worked answer beside it (2 points) | 3 |
| Reflection: what the container made you notice (1 point), and what `safe-and-private` said and what you did (2 points) | 3 |
