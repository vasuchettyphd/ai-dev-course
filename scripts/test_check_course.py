# scripts/test_check_course.py
import pathlib, tempfile, unittest
from check_course import check, WEEKS, ADVANCED

STUB = "# Week\n\nStatus: coming soon\n"
RUBRIC10 = "| Criterion | Points |\n|---|---|\n| Works | 6 |\n| Explained | 4 |\n"
RUBRIC30 = "| Criterion | Points |\n|---|---|\n| Demo | 20 |\n| Write-up | 10 |\n"


def make_course(root):
    for w in WEEKS:
        (root / "weeks" / w).mkdir(parents=True)
        (root / "weeks" / w / "README.md").write_text(STUB)
    for a in ADVANCED:
        (root / "advanced" / a).mkdir(parents=True)
        (root / "advanced" / a / "README.md").write_text("# T\n")
    (root / "README.md").write_text("# Course\n")
    (root / ".gitattributes").write_text("*.sh text eol=lf\n")


class CheckCourse(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        make_course(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_course_passes(self):
        self.assertEqual(check(self.root), [])

    def test_missing_week_folder(self):
        (self.root / "weeks" / "05-building-with-ai" / "README.md").unlink()
        (self.root / "weeks" / "05-building-with-ai").rmdir()
        self.assertTrue(any("05-building-with-ai" in p for p in check(self.root)))

    def test_finished_week_needs_slides_and_assignment(self):
        (self.root / "weeks" / "01-what-is-ai" / "README.md").write_text("# Week 1\n")
        problems = check(self.root)
        self.assertTrue(any("slides.md" in p for p in problems))
        self.assertTrue(any("assignment.md" in p for p in problems))

    def test_rubric_must_total_10(self):
        w = self.root / "weeks" / "01-what-is-ai"
        (w / "README.md").write_text("# Week 1\n")
        (w / "slides.md").write_text("# s\n")
        (w / "assignment.md").write_text(RUBRIC10.replace("| 4 |", "| 3 |"))
        self.assertTrue(any("total 9" in p for p in check(self.root)))
        (w / "assignment.md").write_text(RUBRIC10)
        self.assertEqual(check(self.root), [])

    def test_week_14_rubric_totals_30(self):
        w = self.root / "weeks" / "14-final-demos"
        (w / "README.md").write_text("# Week 14\n")
        (w / "slides.md").write_text("# s\n")
        (w / "assignment.md").write_text(RUBRIC30)
        self.assertEqual(check(self.root), [])

    def test_em_dash_caught_anywhere(self):
        (self.root / "advanced" / "dbt" / "notes.py").write_text("x = 1  # a \u2014 b\n")
        self.assertTrue(any("em dash" in p for p in check(self.root)))

    def test_broken_relative_link(self):
        (self.root / "README.md").write_text("[w](weeks/99-nope/)\n[ok](weeks/01-what-is-ai/)\n[web](https://x.y)\n")
        problems = check(self.root)
        self.assertEqual(len(problems), 1)
        self.assertIn("weeks/99-nope/", problems[0])

    def test_old_numbered_tutorial_path(self):
        (self.root / "advanced" / "dbt" / "README.md").write_text("cd ai-dev-course/01-dbt\n")
        self.assertTrue(any("old path" in p for p in check(self.root)))

    def test_docs_may_mention_old_paths_and_example_links(self):
        (self.root / "docs").mkdir()
        (self.root / "docs" / "plan.md").write_text("Move `01-dbt`, see [x](weeks/99-nope/)\n")
        self.assertEqual(check(self.root), [])

    def test_shell_scripts_need_lf_rule(self):
        (self.root / ".gitattributes").write_text("")
        (self.root / "advanced" / "beads" / "run.sh").write_text("echo hi\n")
        self.assertTrue(any("eol=lf" in p for p in check(self.root)))

    def test_utf8_em_dash_in_markdown_caught(self):
        (self.root / "advanced" / "dbt" / "README.md").write_text("a \u2014 b\n", encoding="utf-8")
        self.assertTrue(any("em dash" in p for p in check(self.root)))

    def test_dot_directories_are_skipped(self):
        (self.root / ".superpowers").mkdir()
        (self.root / ".superpowers" / "x.md").write_text(
            "Move `01-dbt`, see [x](weeks/99-nope/) and a \u2014 dash\n", encoding="utf-8")
        self.assertEqual(check(self.root), [])

    def test_dot_files_are_not_skipped(self):
        (self.root / ".notes.md").write_text("a \u2014 b\n", encoding="utf-8")
        self.assertTrue(any("em dash" in p for p in check(self.root)))

    def test_notebook_em_dash_caught(self):
        (self.root / "advanced" / "dbt" / "analysis.ipynb").write_text(
            '{"cells": [{"source": "a \u2014 b"}]}\n', encoding="utf-8")
        self.assertTrue(any("em dash" in p for p in check(self.root)))

    def test_link_inside_code_fence_not_checked(self):
        (self.root / "README.md").write_text("```\n[w](weeks/99-nope/)\n```\n")
        self.assertEqual(check(self.root), [])

    def test_link_inside_inline_code_not_checked(self):
        (self.root / "README.md").write_text("Use `[w](weeks/99-nope/)` syntax.\n")
        self.assertEqual(check(self.root), [])

    def test_percent_encoded_link_resolves_to_decoded_name(self):
        (self.root / "README.md").write_text("[a](my%20file.md)\n")
        self.assertTrue(any("my file.md" in p for p in check(self.root)))
        (self.root / "my file.md").write_text("# hi\n")
        self.assertEqual(check(self.root), [])

    def test_root_relative_link_resolves_against_repo_root(self):
        (self.root / "advanced" / "dbt" / "README.md").write_text("[b](/README.md)\n")
        self.assertEqual(check(self.root), [])
        (self.root / "advanced" / "dbt" / "README.md").write_text("[b](/nope.md)\n")
        self.assertTrue(any("/nope.md" in p for p in check(self.root)))

    def test_scheme_links_are_skipped_case_insensitively(self):
        (self.root / "README.md").write_text("[c](HTTP://x.y) [m](mailto:a@b.c)\n")
        self.assertEqual(check(self.root), [])

    def test_total_row_is_ignored_in_rubric(self):
        w = self.root / "weeks" / "01-what-is-ai"
        (w / "README.md").write_text("# Week 1\n")
        (w / "slides.md").write_text("# s\n")
        (w / "assignment.md").write_text(RUBRIC10 + "| Total | 10 |\n")
        self.assertEqual(check(self.root), [])


if __name__ == "__main__":
    unittest.main()
