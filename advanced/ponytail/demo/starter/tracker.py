"""A tiny expense tracker.

Usage:
    python3 tracker.py list  [--file expenses.csv]
    python3 tracker.py total [--file expenses.csv]
"""
import argparse
import csv
from datetime import date
from decimal import Decimal


def load_expenses(path):
    """Read the CSV into a list of dicts with real date and Decimal values."""
    with open(path, newline="") as f:
        return [
            {
                "date": date.fromisoformat(row["date"]),
                "category": row["category"],
                "amount": Decimal(row["amount"]),
                "note": row["note"],
            }
            for row in csv.DictReader(f)
        ]


def format_money(amount):
    """Format a Decimal as dollars, e.g. Decimal('1234.5') -> '$1,234.50'."""
    return f"${amount:,.2f}"


def cmd_list(expenses):
    for e in expenses:
        print(f"{e['date']}  {e['category']:<12} {format_money(e['amount']):>10}  {e['note']}")


def cmd_total(expenses):
    print(f"Total: {format_money(sum(e['amount'] for e in expenses))}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="A tiny expense tracker.")
    parser.add_argument("--file", default="expenses.csv")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="show every expense")
    sub.add_parser("total", help="show the total spent")
    args = parser.parse_args(argv)

    expenses = load_expenses(args.file)
    if args.command == "list":
        cmd_list(expenses)
    elif args.command == "total":
        cmd_total(expenses)


if __name__ == "__main__":
    main()
