# Working on the course

- **New week:** copy the three files in `templates/` into the week folder. Copying the template README replaces the stub, so there is no Status line left to remove.
- **Slides:** slides build in Docker, so Docker must be running; the first run downloads the Marp image. Run `npm run slides` (or `sh scripts/build-slides.sh` without npm) to build every `weeks/*/slides.md` into `slides.pdf` next to it. Commit each `slides.pdf` as well, so students can open it without installing anything. On Windows, run the slide build from WSL.
- **Before every PR:** run `python3 scripts/check_course.py`. It must print `OK`. It checks the week layout, rubric totals (10 points, or 30 for week 14), relative links, old tutorial paths, shell-script line endings and em dashes. When you change the checker, also run `cd scripts && python3 -m unittest test_check_course`.
- **Rubric format:** a table under the `## Rubric` heading in `assignment.md`, with the points in the last column.
- **Style:** plain language for students who don't code, every command shown with its expected output, the tested tool versions listed at the top, and no em dashes.
