# Bugs

Bugs found in the deal screener, one section each, newest last.

## Bug 1: Interest rate typed as 0.07 is read as 0.07%

- **Found by:** the instructor, acting as a classmate, on 2026-10-12, using the odd-input list from the feedback form
- **What I did (exact input):** listing B (price 150000, rent 1700, tax 2400, insurance 1200, HOA 0, down payment 25, loan term 30, closing costs 6000), with `0.07` typed for the interest rate instead of `7`
- **What I expected:** a monthly mortgage payment of about $748.47, the 7% figure worked out by hand, or a question asking whether I meant 7%
- **What happened:** no question. It took the rate as 0.07%: monthly mortgage payment $315.80 (not $748.47), monthly cash flow $863.20 (not $430.53), cash-on-cash return 23.81% (not 11.88%). The verdict was Overall: PASS, the same as with `7`, so only the numbers show the mistake.
- **Does it happen every time?** Yes
- **Status:** Open
- **Cause:** (fill in once you know)
