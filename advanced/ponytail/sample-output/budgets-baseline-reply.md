I added a `budget` command to the tracker. It warns for every month a category went over its limit. The tests pass, including two new ones for this.

Limits live in a new `budgets.csv` (`category,monthly_limit`). Each limit applies to every calendar month, and categories without a row aren't checked. I set starter values of groceries $200, eating out $40 and transport $50, so change those to your real budgets.

Running it on your current data gives:

```
$ python3 tracker.py budget
WARNING 2026-09 eating out: $50.50 spent, $10.50 over the $40.00 budget
```

If nothing is over, it prints "All categories are within budget."

You have to run `budget` yourself. The warning doesn't appear when you run `list` or `total`, and nothing runs it automatically. If you want it to show up on every run, or to check the current month only, say so and I'll add it. The code is in `tracker.py` and the tests are in `test_tracker.py`. Nothing is committed.
