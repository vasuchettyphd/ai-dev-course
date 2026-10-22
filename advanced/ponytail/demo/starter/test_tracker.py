import io
import unittest
from contextlib import redirect_stdout
from decimal import Decimal

import tracker


class TrackerTests(unittest.TestCase):
    def test_load_expenses_parses_amounts(self):
        expenses = tracker.load_expenses("expenses.csv")
        self.assertEqual(len(expenses), 12)
        self.assertEqual(expenses[0]["amount"], Decimal("54.20"))

    def test_format_money(self):
        self.assertEqual(tracker.format_money(Decimal("1234.5")), "$1,234.50")

    def test_total_command(self):
        out = io.StringIO()
        with redirect_stdout(out):
            tracker.main(["total"])
        self.assertEqual(out.getvalue().strip(), "Total: $2,235.05")


if __name__ == "__main__":
    unittest.main()
