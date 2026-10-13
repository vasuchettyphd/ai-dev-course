# Evaluation of the listing step (week 12)

This folder checks how well the listing step (`dealscreener/extract.py`, from week 9) reads a listing. It holds 20 made-up listings and, for each one, the five numbers a careful person would type in. The program runs the model on every listing and counts how many numbers it got right.

Every listing is a **fictional listing written for this course example**: no real people, addresses or phone numbers.

**The answers came first.** The 20 listings, `expected.json` and this scoring rule were written and committed before the model saw any of them. The git history shows that commit before the first results file. The expected answers are never changed to raise the score: a change is allowed only to fix a real mistake in an answer, and it is recorded under [Corrections](#corrections) with the reason.

## What's here

- `listings/case-01.txt` to `listings/case-20.txt`: the listings.
- `expected.json`: one entry per listing, with its id, its file, whether it is held out, its category, the five expected numbers, and a note saying why those are the right answers. `null` means "the listing doesn't state this number".
- `results/`: one Markdown file per run, named `<date>-<which>.md` (`dev`, `held-out` or `all`); a second run of the same kind on the same day gets `-2`, then `-3`, so nothing is overwritten. Each holds the date, the model, the score, a table of the misses, any errors and the cost. No keys.

## The 20 cases

| Category | How many | Cases | What it tests |
|---|---|---|---|
| `clean` | 4 | 01 to 04 | all five numbers stated plainly |
| `messy` | 4 | 05 to 08 | tax given monthly, insurance given monthly, "price reduced from", HOA called "association dues" (and given per quarter) |
| `missing` | 4 | 09 to 12 | numbers the listing doesn't state: the answer is `null` |
| `trap` | 3 | 13 to 15 | a yearly rent, a price range ("offers between"), two prices (list price and appraisal) |
| `extra_numbers` | 3 | 16 to 18 | numbers that aren't inputs: square feet, year built, bedrooms, a phone number, a security deposit, a seller credit (case 18 also gives the HOA per year) |
| `no_hoa_words` | 2 | 19 and 20 | "no HOA" said in words: the answer is 0 |

Two cases test rules the week 9 instructions don't spell out: a quarterly HOA (case 08) and a yearly HOA (case 18). The instructions say the HOA is per month, so the right answer is the monthly amount.

## Dev cases and held-out cases

Five cases are **held out**: 03 (clean), 07 (messy), 11 (missing), 14 (trap) and 17 (extra numbers). The other 15 are the **dev cases**. Look at the dev results as often as you like and change the program because of them. Run the held-out cases once, after your one change, and report what you get. If you change the program because of a held-out miss, those cases stop telling you anything new.

## The scoring rule

- Each case has five fields: `purchase_price`, `monthly_rent`, `yearly_property_tax`, `yearly_insurance`, `monthly_hoa`.
- A field is **right** when:
  - the expected answer is `null` and the model gave `null`, or
  - both are numbers and they differ by **$1.00 or less** (so 2220 and 2220.5 match; 2220 and 2221.01 don't).
- A field is **wrong** when one is `null` and the other is a number, or the numbers differ by more than $1.00. A number where `null` was expected is a guess, and counts as wrong.
- The model's number is the one `extract.py` keeps: anything that isn't a number of 0 or more is already turned into `null` by the program, and it is scored as `null`.
- A case that fails with an **error** (no reply, too many requests, a cut-off answer) scores no fields. It is listed under errors and left out of the field count, so the score is "N of M fields right" over the cases that ran.
- The score lines are:
  - `Score: N of M fields right (P%), K of C cases fully right. Errors: E.`
  - `Cost: about $X.` from the token counts and the published price in `extract.py`.

## What 20 cases can and can't show

Anthropic's guidance on evaluations ([Anthropic: develop tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests), read 13 October 2026) says to "Prioritize volume over quality", and its examples use from 50 to 10,000 cases. This set does the opposite on purpose: 20 cases, each written and checked by hand, so you can read every listing and every answer yourself.

Twenty cases can show gross failures (a whole kind of listing the model gets wrong) and patterns (the same mistake in several cases). They can't give a precise accuracy rate: one case is 5 points out of 100%, so 17 of 20 and 18 of 20 are the same result within the noise. The same run twice can also give different answers, because the model doesn't answer the same way every time. In the course's runs, case 14 (a price range) got 187500 in the held-out run and `null` in the `--all` run.

## How to run it

From the `example-project` folder, with the key in your environment (see the main README):

```
python3 -m dealscreener.evaluate              # the 15 dev cases
python3 -m dealscreener.evaluate --held-out   # the 5 held-out cases, once, after your change
python3 -m dealscreener.evaluate --all        # all 20
```

## Corrections

None so far.
