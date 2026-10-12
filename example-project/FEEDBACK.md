# Feedback form: deal screener (example)

*Written by the instructor acting as the classmate, to show what a filled-in form looks like. In class, your classmate fills this in during your demo.*

**Project:** rental deal screener (the course's example project)
**Owner:** the instructor
**Classmate:** the instructor, acting as a classmate
**Date:** 2026-10-12

## What I tried (exact inputs)

I used several inputs from the odd-input list on the feedback form, as well as my own.

- Listing B as the README gives it: 150000, 1700, 2400, 1200, 0, 25, 7, 30, 6000.
- A blank answer (pressed Enter too early) for the purchase price.
- Words instead of numbers: `abc` for the purchase price.
- `0` for the purchase price, and `-5` for the purchase price.
- A very large number: `1e308` for the purchase price.
- Symbols: `$150,000` for the price and `25%` for the down payment.
- `30.5` for the loan term (a decimal where a whole number is expected).
- `0.07` for the interest rate instead of `7` (a decimal where a whole percentage is expected).

## What worked

- Listing B gave a monthly cash flow of $430.53 and Overall: PASS, matching the README.
- Blank answers, words, `0` for the price, negative numbers and the very large number were each asked again with a plain message, and no error screen.
- `$`, `,` and `%` were accepted and ignored.
- `30.5` years was asked again: "Please type a whole number of years, 1 or more."

## What broke, and exactly how

- **What I typed:** listing B, but `0.07` for the interest rate instead of `7`.
- **What I expected:** a monthly mortgage payment of about $748.47 (the 7% figure), or a question asking if I meant 7%.
- **What happened:** no question. It read the rate as 0.07%. Monthly mortgage payment $315.80 (not $748.47), monthly cash flow $863.20 (not $430.53), cash-on-cash return 23.81% (not 11.88%). It still said Overall: PASS, so only the numbers showed something was wrong.

## One suggestion

When a percentage is typed as a decimal like `0.07`, ask whether I meant 7% instead of guessing.

## For the owner: bugs added to BUGS.md

- Bug 1: Interest rate typed as 0.07 is read as 0.07%.
