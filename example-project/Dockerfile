# Start from the official Python image. 3.12 keeps Python on version 3.12 (it still gets
# small fixes); never use "latest", which can change under you. The course uses
# python:3.12-slim: "slim" leaves out extras the program doesn't use.
FROM python:3.12-slim

# Work in a folder called /app inside the container.
WORKDIR /app

# No package install step: the program uses only Python's standard library. A project that
# needs packages first copies its list of packages (requirements.txt for Python,
# package.json for Node.js) and installs them here (pip install -r requirements.txt, or
# npm install), before the line below, so Docker can reuse that step when only your code changes.

# Copy this folder into /app, leaving out everything listed in .dockerignore.
COPY . .

# Run as "nobody", a user with no special powers, instead of the all-powerful root user
# (optional: if your own program writes files inside /app and gets "Permission denied",
# remove this line or ask Claude).
USER nobody

# The command that runs when the container starts: the deal screener.
CMD ["python", "-m", "dealscreener"]
