import unittest


class Placeholder(unittest.TestCase):
    def test_package_imports(self):
        import wordstats  # noqa: F401


if __name__ == "__main__":
    unittest.main()
