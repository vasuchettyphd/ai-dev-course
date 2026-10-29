# Demo script: rental deal screener

The instructor's model 3-minute demo, for week 14. Copy its shape for your own project: one row per step, a time for each, the exact command, what to say, and what to do if it fails.

"Terminal" below means: the Terminal on a Mac, or the Ubuntu window on Windows, in the `example-project` folder, with `(.venv)` showing (the virtual environment from week 9).

## Before you start

Do these 10 minutes before your turn, not during it.

1. **Open a new Terminal window with no key loaded.** Don't run `set -a; . ./.env; set +a` in it, and never type `cat .env`, `env` or `printenv` during a demo. The listing step and the agent read `.env` themselves, so the key never needs to be in the window. To check the window holds no key, without showing anything secret:

   Type in: the Terminal.

   ```
   [ -z "$ANTHROPIC_API_KEY$GEMINI_API_KEY" ] && echo "No key loaded"
   ```

   It should print `No key loaded`. If it prints nothing, close the window and open a new one.
2. **`.env` is in place.** `ls .env` prints `.env`, and `git check-ignore .env` prints `.env`. Don't open the file.
3. **Activate the virtual environment:** `source .venv/bin/activate`, so `(.venv)` shows.
4. **Make the terminal font large** (Cmd and + on a Mac, Ctrl and + in the Ubuntu window) so the back row can read it. Clear the screen with `clear`.
5. **Turn notifications off** (Focus or Do Not Disturb) and close every other window and tab: a chat, an email or a key in another tab is on screen the moment you share it.
6. **Open `listings/listing-b.txt` in a text editor** and select all of it, ready to copy and paste.
7. **Run the whole script once** on the day, at the same place, to check the network and the key work. The two live calls cost about $0.001 together (see [What the rehearsal showed](#what-the-rehearsal-showed)).

If a key ever shows on screen, treat it as leaked: delete it in the Anthropic Console first (Settings > API keys), then carry on with the fallback below.

## The script

Each time is when the step starts and ends, counted from 0:00. The last step ends at 3:00. An estimated read-through (the Say column at about 150 words a minute, over the real output below, allowing 10 seconds for each live call) came to about 2:40, which leaves 20 seconds spare. A stopwatch run is being tested.

| Time | Show | Command and where to type it | Say | If it fails |
|---|---|---|---|---|
| 0:00 to 0:15 | Your face, or the README's first lines | None | "Someone buying their first rental property needs to know in a minute whether a listing is worth a closer look. This tool tells them, using their own rules." | Nothing can fail here. |
| 0:15 to 1:05 | The listing step reading listing B, you confirming each number, the verdict | Terminal: `python3 -m dealscreener --listing`, then paste `listings/listing-b.txt`, type `done` and press Enter. Press Enter five times to keep the listing's numbers, then type `25`, `7`, `30`, `6000` for the loan. | "A model reads the listing and offers five numbers; I check each one. The verdict: PASS, $430.53 a month of cash flow." | If it says "For now, type the numbers yourself.", type them: 150000, 1700, 2400, 1200, 0, then 25, 7, 30, 6000. Say: "The model call failed, so it falls back to typing. The maths doesn't need the model." |
| 1:05 to 1:45 | The agent calling the calculator tool, and the same numbers in its answer | Terminal: `python3 -m dealscreener.agent "Should I buy this rental? The price is \$150,000 and the rent is \$1,700 a month. Property tax is \$2,400 a year, insurance is \$1,200 a year and there is no HOA fee. I'd put 25% down on a 30-year loan at 7% interest, with \$6,000 in closing costs."` (paste it from this file; don't type it) | "Here I just ask in plain English. Claude doesn't do the sums: it calls my calculator, so the $430.53 is the same as before." | If it prints an error sentence, show the course's run in the README ([How to ask the agent](README.md#how-to-ask-the-agent)) and say: "The call failed; this is the answer from the course's run." |
| 1:45 to 2:20 | The committed evaluation results: week 12, then week 13 before and after | Terminal: `head -7 evals/results/2026-10-13-all.md`, then `head -7 evals/results/2026-10-13-injection.md evals/results/2026-10-13-injection-3.md` | "On 20 made-up listings, with the answers written first, it got 100 of 100 numbers right. Of 8 hostile listings, one attack worked before my fix and none after." (These are the saved runs: the model answers a little differently each time, so the file is the record.) | These need no key and no network, so they work offline. If the terminal misbehaves, open the same files in a text editor. |
| 2:20 to 2:45 | One honest limit: case 14 answered two ways | Terminal: `grep case-14 evals/results/2026-10-13-held-out.md evals/results/2026-10-13-all.md` | "Case 14 gives a price range: once the model guessed 187500, later it said there's no single price. One run isn't the last word, so I confirm every number." | Works offline. |
| 2:45 to 3:00 | Close | None | "Claude Code wrote nearly all the code and tests, from plans I approved. I decided the plan and the rules, checked the answers, and decided which fixes to make." | Nothing can fail here. |

### You'll see

These are the real outputs from the rehearsal, shortened with "..." where long.

**0:15, the listing step** (after you paste and type `done`):

```
Asking the model to read the listing...
Used 978 input and 65 output tokens, about $0.00013.
Check each number from the listing: press Enter to keep it, or type the right number.
Purchase price ($) [from the listing: 150000]:
Monthly rent ($) [from the listing: 1700]:
Yearly property tax ($) [from the listing: 2400]:
Yearly insurance ($) [from the listing: 1200]:
Monthly HOA fee ($, 0 if none) [from the listing: 0]:
Down payment (%): 25
Interest rate (%): 7
Loan term (years): 30
Closing costs ($): 6000

Monthly mortgage payment: $748.47
Monthly cash flow: $430.53
Cap rate: 9.43%
Cash-on-cash return: 11.88%

PASS  Cash-on-cash return 11.88% is at least 10.00%
PASS  Monthly cash flow $430.53 is at least $100.00

Overall: PASS
```

**1:05, the agent:**

```
Calling screen_listing with {"purchase_price":150000,"monthly_rent":1700,"yearly_property_tax":2400,"yearly_insurance":1200,"monthly_hoa":0,"down_payment_pct":25,"interest_rate_pct":7,"loan_term_years":30,"closing_costs":6000}

The screen says this listing **passes** your buy box rules. Here are the results:

- **Monthly mortgage payment:** $748.47
- **Monthly cash flow:** $430.53. ...
- **Cap rate:** 9.43%. ...
- **Cash-on-cash return:** 11.88%. ...

...

Used 3072 input and 1005 output tokens on Claude in 2 turns, about $0.00081.
```

Claude's wording is different every time. Point at the `Calling screen_listing with` line and the four numbers: those come from the calculator, so they don't change.

**1:45, the evaluation:**

```
- Set: all (20 cases)
- Score: 100 of 100 fields right (100%), 20 of 20 cases fully right. Errors: 0.
...
==> evals/results/2026-10-13-injection.md <==
...
- Score: 39 of 40 fields right (98%), 7 of 8 cases fully right. Errors: 0.
...
==> evals/results/2026-10-13-injection-3.md <==
...
- Score: 40 of 40 fields right (100%), 8 of 8 cases fully right. Errors: 0.
```

**2:20, case 14:**

```
evals/results/2026-10-13-held-out.md:| case-14 | trap | purchase_price | null | 187500 |
evals/results/2026-10-13-held-out.md:| case-14 | trap | 4/5 |
evals/results/2026-10-13-all.md:| case-14 | trap | 5/5 |
```

Read it out: in the held-out run the right answer was `null` (no single price) and the model gave 187500; in the run of all 20 it got all 5 numbers right.

## If it fails

No internet, a "too many requests" error, a key that stopped working, or a call that hangs for more than 10 seconds: don't fix it in front of the room. Press Ctrl+C if it hangs, say in one sentence what failed, and switch to the offline fallback. It needs no key and no network.

Type in: the Terminal.

```
python3 -m unittest
```

You'll see (the dots are cut short here):

```
Ran 236 tests in 0.062s

OK (skipped=4)
```

(The 4 skipped are the live tests, which run only with `RUN_LIVE_TESTS=1`. If the `mcp` package isn't installed, for example on Python 3.10, it says `skipped=9`. Run as root, it skips one more. That's fine.)

Say: "All 236 tests pass with no key and no internet: they use a fake model, so the calculator and the program are checked every time." Then show the results files as in the 1:45 and 2:20 rows: they are committed files, so they work offline too. A demo that fails live is fine if you use the fallback well and say what happened.

## What to cut first if you're over time

1. **The agent step (1:05 to 1:45).** It shows the same $430.53 as the listing step. Cutting it saves 40 seconds; say "it can also answer a plain-English question" in one sentence instead.
2. **The week 12 file in the evaluation step.** Show only the two injection files, before and after.
3. **The loan questions.** If the room is short of time, say the four loan numbers aloud as you type them rather than explaining each one.

Never cut the honest limit (2:20) or the close (2:45): they are worth points, and they take 40 seconds together.

## What the rehearsal showed

Run on 13 October 2026 with Claude Haiku 5.5, in a `python:3.12-slim` container, once each:

| Step | Input tokens | Output tokens | Cost |
|---|---|---|---|
| Listing step, `listing-b.txt` | 978 | 65 | about $0.00013 |
| Agent, listing B question | 3072 | 1005 | about $0.00081 |

The listing step uses more input tokens than in week 9 (887 in the [cost record](README.md#cost-record)) because week 13 sends the listing inside a JSON object with one more sentence of instructions. The offline fallback was run in a container with the network switched off and no key: the 236 tests passed and the results files printed.
