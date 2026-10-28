# Week 9 assignment: Calling a model from code

## What to do

Follow the [week 9 README](README.md) on your own laptop, in your private `semester-project` repo, and collect four things.

On the [Gemini path](gemini.md)? Read its [hand-in differences](gemini.md#hand-in-differences) too.

**(a) Your merged AI feature.** The address of the merged pull request from your `ai-feature` branch (README steps 5 to 7). Its **Files changed** must show:

- the feature's code, with the key read only from the environment;
- tests that use a fake model and pass with no key, including a test for "no key";
- the package list (`requirements.txt` or `package.json`) with the version pinned, and the Dockerfile installing it;
- `.env.example` with a **fake** key, and your README saying how to set up `.env`;
- `REVIEW.md` with the week 9 section.

**No `.env` file and no real key**, anywhere in the pull request or the repo's history. The repo stays **private**, with `vasuchettyphd` as a collaborator.

**(b) A cost log of three real calls** (README step 5f). For each call: what it was for, the input tokens, the output tokens, and the cost you worked out from them with the model's prices (show the arithmetic once, as in README step 1). Add a screenshot of the Console's **Usage** page that roughly matches, with nothing secret on it.

**(c) Two screenshots** (README step 5e): your feature working with the key loaded, and your program without a key, saying so and carrying on. Check that no key is visible in either.

**(d) A short reflection,** about half a page:

1. **Which model, and why:** which model you used, what one call cost you, and whether a dearer model would be worth it for your feature.
2. **Dependable answers:** current models don't let you set temperature (README step 4a), so how did you make your feature's answers dependable? Say what your prompt asks for, whether you used structured output, and what your code checks before using an answer. Give one example of an answer the model got wrong, or could get wrong, and what your program does about it.

Never put an API key, a password, a sign-in code or anything from your `.env` file in your hand-in. If you think a key got into your hand-in or your repo, delete it in the Console first (README step 2f).

## What to hand in

- One document with the pull request's address, the cost log with its screenshot, the two screenshots and your reflection.

Submit it the way your course site says.

## Rubric

| Criterion | Points |
|---|---|
| Merged AI feature pull request: tests use a fake model and include a "no key" test, the package is pinned, and no key or `.env` anywhere | 4 |
| Cost log of three real calls, with tokens and a cost worked out from them | 2 |
| Screenshots of the feature working and of the no-key fallback | 2 |
| Reflection: which model and why (1 point), and how you made its answers dependable (1 point) | 2 |
