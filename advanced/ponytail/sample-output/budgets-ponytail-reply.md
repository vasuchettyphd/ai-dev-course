I added a `budget` command that warns for each category and month where you went over your limit. The tests pass.

- **Setting limits:** `budgets.csv` holds a monthly limit per category. The limits in it are placeholders I picked, so edit them.
- **Running it:** `python3 tracker.py budget` prints one `OVER BUDGET` line per overspend, or "All within budget."

On your current data it prints:
```
OVER BUDGET 2026-09 eating out: $50.50 of $40.00 (+$10.50)
OVER BUDGET 2026-09 groceries: $164.15 of $150.00 (+$14.15)
OVER BUDGET 2026-10 transport: $45.00 of $40.00 (+$5.00)
```

**Skipped:**
- The warning only shows when you run `budget`, not when you add an expense. This tracker has no add command yet.
- Categories missing from `budgets.csv` are ignored, with no warning.
- A malformed budgets file raises a plain Python error.
