#!/bin/sh
# Build slide decks to PDF with Marp in Docker. Run from anywhere: it works on this repo's weeks.
# With no arguments, builds every weeks/*/slides.md. Each slides.pdf lands next to its slides.md.
cd "$(dirname "$0")/.." || exit 1
if [ "$#" -eq 0 ]; then
  set -- weeks/*/slides.md
  if [ ! -e "$1" ]; then
    echo "no slides yet"
    exit 0
  fi
fi
if ! command -v docker >/dev/null 2>&1; then
  echo "docker not found on PATH: install Docker and start it, then try again" >&2
  exit 1
fi
docker info >/dev/null 2>&1 || { echo "Docker is installed but not running: start Docker Desktop and try again" >&2; exit 1; }
docker run --rm --init -v "$PWD":/home/marp/app -e MARP_USER="$(id -u):$(id -g)" marpteam/marp-cli:v4.1.2 --pdf --allow-local-files "$@"
