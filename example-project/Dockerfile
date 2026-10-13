# Start from the official Python image. 3.12 keeps Python on version 3.12 (it still gets
# small fixes); never use "latest", which can change under you. The course uses
# python:3.12-slim: "slim" leaves out extras the program doesn't use.
FROM python:3.12-slim

# Work in a folder called /app inside the container.
WORKDIR /app

# Copy the list of packages first, on its own, and install them. The listing step (week 9),
# the notes command (week 10) and the agent and MCP server (week 11) need three packages:
# anthropic (for Claude), google-genai (for Google's embeddings) and mcp (for the MCP
# server). Doing this before
# copying the code lets Docker reuse this slow step when only your code changes.
# --no-cache-dir stops pip keeping its download files, so the image stays smaller.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy this folder into /app, leaving out everything listed in .dockerignore.
COPY . .

# Run as "nobody", a user with no special powers, instead of the all-powerful root user
# (optional: if your own program writes files inside /app and gets "Permission denied",
# remove this line or ask Claude).
USER nobody

# The command that runs when the container starts: the deal screener. To paste a listing
# first, add the key at run time (never in the image) and the flag:
#   docker run -it --rm --env-file .env dealscreener python -m dealscreener --listing
CMD ["python", "-m", "dealscreener"]
