# Working on the course

- **New week:** copy the three files in `templates/` into the week folder and remove the `Status: coming soon` line from its README.
- **Slides:** slides build in Docker, so Docker must be running; the first run downloads the Marp image. Run `npm run slides` (or `sh scripts/build-slides.sh` without npm) to build every `weeks/*/slides.md` into `slides.pdf` next to it. Commit each `slides.pdf` as well, so students can open it without installing anything.
- **Before every PR:** run `python3 scripts/check_course.py`. It must print `OK`. It checks the week layout, rubric totals (10 points, or 30 for week 14), relative links, old tutorial paths, shell-script line endings and em dashes.
- **Style:** plain language for students who don't code, every command shown with its expected output, the tested tool versions listed at the top, and no em dashes.
