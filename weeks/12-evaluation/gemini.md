# Week 12 on the Gemini path

This page is for you if your instructor put you on the **Gemini path** in week 9 (Google's free tier with `gemini-3.5-flash-lite`, instead of paid Claude API credit; see [week 9 on the Gemini path](../09-calling-a-model/gemini.md)). Your own AI feature already runs on Gemini, so almost all of week 12 is the same. Follow the [week 12 README](README.md) as written, with the changes below. Everything not mentioned here (the honesty rules, the Claude Code answers table, the branch, the merge commit) stays exactly as it is.

**Tested with** (28 October 2026): `google-genai` 2.30.0 and `gemini-3.5-flash-lite` on the free tier, for single calls (week 9). **Being tested:** a full 20-case evaluation run on the free tier.

## Cost and limits

Everything this week is free. You make about 50 calls for your own runs (an estimate: three dev runs and one held-out run), and Google's free tier charges nothing for them. You don't run the deal screener in step 3 (see below), so there are no other calls.

The catch is the free tier's limits. Google limits how many requests you can make per minute and per day; Google says "View your active rate limits in AI Studio" (<https://ai.google.dev/gemini-api/docs/rate-limits>, read 28 October 2026). A 20-case run sends calls quickly, one after another, so you may hit the per-minute limit partway through. Error **429** means "too many requests": wait and try again. The daily count resets at midnight Pacific time.

Remember the free tier's other cost from week 10: Google uses what you send to improve its products. Your 20 test cases go to Google, so they must be course-safe (step 4d already says so; on this path it matters even more).

## Step by step

**Steps 1 and 2:** the same. Read them as written.

**Step 3, the deal screener's evaluation:** don't run it. The deal screener uses Claude for its listing step, so `python3 -m dealscreener.evaluate` needs a Claude key, which you don't have. Instead, read the course's recorded results in step 3b and the case 14 miss in step 3c. The lesson stands without running it: the same listing got two different answers in two runs, so one good run proves little. Your own runs in step 6 will show you the same thing on Gemini.

**Step 4, your test set:** the same.

**Step 5, the evaluation script:** use the same planning prompt, with two changes:

1. Replace `and print one line per case, the score, the misses and the cost.` with:

   ```text
   and print one line per case, the score, the misses, the input and output tokens for the run, and the cost: $0 on the free tier, plus what the run would cost on the paid tier ($0.30 per million input tokens, $2.50 per million output tokens, counting thinking tokens as output).
   ```

2. Add this sentence just before `I'm not a programmer`:

   ```text
   If a call fails with a 429 or 503 error, wait and retry it once; if it still fails, record that case as an error with a plain sentence and carry on.
   ```

Everything else in the prompt stays: never change the test cases, dev cases by default, `--held-out` only once, stop if there's no API key, save results without a key, read the key only from the environment, never read `.env`, offline tests with a fake model.

**Step 6, run it:** the same. Load your key the way your feature's README says (for most of you, `set -a; . ./.env; set +a` in the folder with `.env`, as in week 9). Your cost lines show $0 with token counts.

**A note on timing.** Like any model, Gemini can answer the same case differently from one run to the next, and the free tier may behave differently from one day to another (Google can change it). So run your two dev runs, your change and your re-run close together, on the same day if you can. If your scores change between days, say so in your report rather than guessing why.

**Step 7, review and finish:** the same, except the key searches. In **Files changed**, use the browser's Find for `AIza` (how Google keys start) and `GEMINI_API_KEY=`, including in the results files, instead of `sk-ant-` and `ANTHROPIC_API_KEY=`. Merge with "Create a merge commit", as the README says.

## What's different in the hand-in

The [assignment](assignment.md) is the same, with the same points. One difference: in part (c)1, report each run's cost as **$0 (free tier)** with its input and output tokens. You can also give the paid-tier figure your script works out. Your report should still say what your score does and doesn't tell you, as everyone's does.

## Troubleshooting

| What you see | What to do |
|---|---|
| ERROR on some cases partway through, with 429 | You hit the free tier's per-minute limit. Your script waits and retries once; if cases still fail, wait a minute and run again. The score counts only the cases that ran: say so in your report. |
| ERROR with 503 UNAVAILABLE, "This model is currently experiencing high demand" | Google's model is busy for a while. Wait a minute and run again; your script records the case as an error and carries on. |
| Most cases fail with 429, even after waiting a few minutes | You've probably reached the daily limit. Run the rest tomorrow: the daily count resets at midnight Pacific time. Check your limits in AI Studio. |
| `No API key was provided` | The key isn't loaded: in the folder with `.env`, run `set -a; . ./.env; set +a`, and check `grep -c '^GEMINI_API_KEY=' .env` prints `1`. |
| `API key not valid` | Check the `GEMINI_API_KEY=` line in `.env`, or make a new key (week 10 step 2b). |
| Anything else | See the [week 12 README's Troubleshooting](README.md#troubleshooting) and [week 9 on the Gemini path](../09-calling-a-model/gemini.md). |
