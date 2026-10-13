---
marp: true
paginate: true
title: Week 14 - Final demos
style: |
  section { font-size: 28px; }
  table { font-size: 21px; }
  pre { font-size: 19px; }
  .small { font-size: 20px; color: #555; }
---

# Week 14: Final demos

AI Development Course

Show what you built

<p class="small">The deal screener's DEMO.md was run for real on 13 October 2026, and its fallback with the network off. A signed-in session, GitHub, and Mac and Windows laptops are being tested.</p>

---

## Today

- What the final demo is
- Get your project ready on `main`
- Write and rehearse a 3-minute demo
- Write `FINAL.md`
- On the day
- The 30-point rubric

---

## The demo rules

1. **No key ever on screen**
2. **Every number is real**, and links to a file
3. **Show one honest limit**
4. **Have a fallback** for when the room's network fails

---

## What you hand in

| Part | Points |
|---|---|
| Your 3-minute demo, in class | 10 |
| Your project as it stands on `main` | 10 |
| `FINAL.md`, about two pages | 10 |

Models: `example-project/DEMO.md` and `example-project/FINAL.md`

---

## Ready on main

- Tests pass with `.env` moved out
- `REVIEW.md`: a Decision and a Reason for every finding
- Week 12 and 13 results committed
- No key anywhere in the history (week 13 step 1)
- The README says how to run it; Docker builds it and runs the tests
- Private repo, your instructor a collaborator

Branch `final`; Claude Code checks the list, **you** fix things.

---

## The deal screener's demo

| Time | Show |
|---|---|
| 0:00 | The problem, in one sentence |
| 0:15 | The listing step on listing B: PASS, $430.53 a month |
| 1:05 | The agent: same answer, from the calculator tool |
| 1:45 | The saved results: week 12, then week 13 before and after |
| 2:20 | One honest limit: case 14, answered two ways |
| 2:45 | What AI did, what I decided |

Rehearsed estimate: about 2:40.

---

## Each row of DEMO.md

Five columns: **Time**, **Show**, **Command and where to type it**, **Say**, **If it fails**

- **Say:** one or two plain sentences
- **If it fails:** what you switch to, and the one sentence you say

---

## The fallback

```bash
python3 -m unittest       # no key, no network
head -7 evals/results/...  # the saved runs
```

The deal screener's fallback ran with the network switched off: all tests ran, every results file opened.

Don't debug in front of the room.

---

## Rehearse

1. Twice with a timer, running the real commands
2. Over time? Cut what `DEMO.md` says to cut first
3. Keep the AI step and the honest limit
4. Once with the fallback

Say less, don't talk faster.

---

## FINAL.md: seven headings

1. What it does and who it's for
2. How it's built, and which parts are AI
3. What I measured
4. What went wrong and what I changed
5. Risks and responsible use
6. What AI did and what I decided
7. What I'd do next

---

## Every number links to a file

- Claude Code drafts it from **your** repo
- A number with no file: **leave it out**
- Then you rewrite it in your own words
- Click every link

---

## Heading 6 matters most

> Claude Code wrote nearly all of the code, the tests, the evaluation cases and most of the text in this folder, working from plans that I approved

- What did AI write?
- What did **you** decide: the plan, the rules, the fixes?
- What would you do differently?

---

## On the day

- A window with **no key loaded**
- Large text; notifications off; other tabs closed
- `DEMO.md` on paper or your phone, not on screen
- A step fails: one sentence, then the fallback
- A key shows: keep going; delete it straight after

---

## The rubric (30)

| Criterion | Points |
|---|---|
| Demo: works or good fallback 4, AI feature 2, honest limit 2, on time 2 | 10 |
| Project on main: tests 2, REVIEW.md 2, results 2, no key 2, run and Docker 2 | 10 |
| Write-up: seven headings 4, numbers traceable 3, heading 6 honest 3 | 10 |

---

## Fourteen weeks

From "what is a model?" to a tested, reviewed, evaluated and secured AI feature, merged through pull requests.

Thank you, and good luck with your demos.
