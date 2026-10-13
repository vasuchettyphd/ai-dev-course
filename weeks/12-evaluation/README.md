# Week 12: Evaluation

**Goal:** find out how well your AI feature really works, with evidence instead of impressions. You'll read how the course measured another model (Jev), watch the deal screener's listing step get scored on 20 test cases, build your own 20-case test set with the right answers written first, write a script that scores your feature, and report what the score does and doesn't tell you, merged through a pull request.

**Time:** plan for about 2 to 3 hours of your own time after class (an estimate); writing good test cases takes longer than people expect. **Cost:** a few Claude calls from your week 9 API credit: running the deal screener's 20 cases once cost under a cent (step 3).

**Tested with** (13 October 2026; these are the versions tested, yours may be newer):

- `anthropic` 1.13.0 and `claude-haiku-5-5`, with real evaluation runs from a container (the scores below are from those runs).
- The deal screener's new evaluation and its tests.
- **Being tested:** everything inside a signed-in Claude Code session, everything on GitHub, and every step on a Mac or in Windows (WSL).

## Before you start

You need:

- Weeks 9 to 11 done: an AI feature in your `semester-project` (week 9, 10 or 11), your keys in `.env`, the `Read(./.env)` deny rule, and the course repo's `example-project` set up with its `.venv` and `.env` (week 10 step 4a).
- `gh` signed in to **your** GitHub account, and Claude Code signed in with your Claude Pro account.

"Your terminal" means **Terminal** on a Mac and the **Ubuntu window** on Windows. As in week 11, start Claude Code only in a window where no key is loaded.

### How you'll work this week

As in weeks 9 to 11: plain-English prompts, plain **Yes** for git, a branch first, a pull request last, and the key rules.

**The evaluation honesty rules, new this week:**

1. **Write the right answers before you run anything.** Commit them first, so your history shows it.
2. **Never change the test set to make the score go up.** If a right answer turns out to be wrong, fix it, and write down why.
3. **Keep 5 cases aside** (the **held-out** cases) and run them only once, after you've made your one change.
4. **Report the misses, not just the score.**
5. **Say what your score can't show.** Twenty cases is a small sample.

| Claude asks to | Choose |
|---|---|
| Create your test cases, expected answers and scoring rule on your `eval` branch | **Yes** |
| Change an expected answer **after** a run | **No**, unless you agree it was a real mistake: then ask it to record the reason |
| Write the evaluation script and its tests | **Yes** |
| Run the evaluation against the real model | **Yes**, in a window you choose: it costs a little credit |
| Read or print `.env`, or put a key in any file (including a results file) | **No** |
| `git add`, `git commit`, `git push` on your `eval` branch, `gh pr create` | plain **Yes**, after `git status` shows no `.env` |
| Anything that changes `main`, or `reset --hard`, `--force`, `git clean`, `rm -rf` | **No** |

## Steps

### 1. "It looked right" isn't evidence

You've tried your AI feature a few times and the answers looked good. That tells you less than it feels like. You probably tried easy cases, you remember the hits better than the misses, and you can't compare one version with the next.

An **evaluation** fixes that. It has four parts:

1. A **test set**: a fixed list of cases, including hard ones.
2. **Expected answers**, decided **before** you run anything, so the model's answer can't sway you.
3. A **scoring rule** that says exactly what counts as right (an exact match, a number within a tolerance, the right category).
4. A **score**, and the list of **misses**, which is where the learning is.

Anthropic's guide (<https://platform.claude.com/docs/en/test-and-evaluate/develop-tests>, read 13 October 2026) says a good success criterion is "Specific: Clearly define what you want to achieve" and "Measurable: Use quantitative metrics or well-defined qualitative scales." It also says to "factor in edge cases", such as "Irrelevant or nonexistent input data" and "Ambiguous test cases where even humans would find it hard to reach an assessment consensus".

**About the size.** Anthropic's guide gives no minimum number of cases; its own examples use from 50 to 10,000, and it says "Prioritize volume over quality: More questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals." This week does the opposite on purpose: 20 cases, each with an answer you wrote and can check yourself. Twenty cases can show **big failures and patterns** ("it always gets yearly rent wrong"). They can't give a precise rate: each case is 5% of the score, so 17 out of 20 against 18 out of 20 is one case, which could be luck.

### 2. Case study: Jev

The course's advanced tutorial [Jev](../../advanced/jev/README.md) measured a model (TypeSafe's Jev 1.13) with about 1,130 real calls, costing "a few cents" in total. Read its README; you don't need to run it. Three lessons from it:

**Small, easy tests look perfect.** On 8 easy support tickets, Jev picked the right team 8 times out of 8, all at confidence 1.00. On a refund policy with 8 cases it got 7 right, and the miss was a $100 refund requested on day 31: it answered "send to a manager" when the rule said deny, and it was 97% confident.

**Errors cluster where the rules bite.** The author then generated 300 cases from a harder four-step refund policy (300 cases from 36 distinct customer messages, one run, with the messages and the right answers written by the author). Asked directly, Jev got 211 of 300 right (70%); with the facts prepared for it first, 236 of 300 (79%); and a hybrid, where code applied the rules and Jev only read the message, got 300 of 300. But for cases within 3 days of a refund window's edge, Jev alone got only 63 of 129 right (49%). The largest single group of its misses (30 of 89) was defective items 366 to 400 days old, which the policy said to deny.

**Confidence isn't correctness.** When the prepared answers were kept only if Jev was at least 90% confident, 174 of 179 were right (97%): better, but 5 confident wrong answers remained.

What that means for you: a feature that looks perfect on a few easy cases can be wrong exactly where it matters, while sounding just as sure. Only a test set with hard cases, scored by a rule you wrote first, shows that.
