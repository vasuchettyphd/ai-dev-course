# Start from the official Python image. 3.12 pins the Python version (never "latest",
# which can change under you); "slim" leaves out extras the program doesn't use.
FROM python:3.12-slim

# Work in a folder called /app inside the container.
WORKDIR /app

# No "pip install" step: the program uses only Python's standard library. A project that
# needs packages copies requirements.txt and runs "pip install -r requirements.txt" here.

# Copy this folder into /app, leaving out everything listed in .dockerignore.
COPY . .

# Run as "nobody", a user with no special powers, instead of the all-powerful root user.
USER nobody

# The command that runs when the container starts: the deal screener.
CMD ["python", "-m", "dealscreener"]
