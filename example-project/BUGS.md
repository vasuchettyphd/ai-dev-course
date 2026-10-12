# Bugs

Bugs found in the deal screener, one section each, newest last.

## Bug 1: Interest rate typed as 0.07 is read as 0.07%

- **Found by:** the instructor, acting as a classmate, on 2026-10-12, using the odd-input list from the feedback form
- **What I did (exact input):** listing B (price 150000, rent 1700, tax 2400, insurance 1200, HOA 0, down payment 25, loan term 30, closing costs 6000), with `0.07` typed for the interest rate instead of `7`
- **What I expected:** a monthly mortgage payment of about $748.47, the 7% figure worked out by hand, or a question asking whether I meant 7%
- **What happened:** no question. It took the rate as 0.07%: monthly mortgage payment $315.80 (not $748.47), monthly cash flow $863.20 (not $430.53), cash-on-cash return 23.81% (not 11.88%). The verdict was Overall: PASS, the same as with `7`, so only the numbers show the mistake.
- **Does it happen every time?** Yes
- **Status:** Fixed in commit `c5d56a2` (the program now asks: "You typed 0.07. Did you mean 7%? Type y for 7%, or n to keep 0.07%:")
- **Cause:** `parse_answer` in `dealscreener/__main__.py` accepts any percent from 0 to 100, so a decimal fraction like 0.07 is taken as a percentage (0.07%). Both percent questions (down payment and interest rate) shared the problem, so the fix covers both: a percent answer between 0 and 1 now gets one follow-up question. The `SmallPercentTest` tests in `tests/test_main.py` failed before the fix and pass after it.
