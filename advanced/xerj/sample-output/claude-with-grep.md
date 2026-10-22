# Claude Code + grep only (baseline)

Captured 2026-10-22 with xerj v1.0.0-rc.98, Claude Code 2.1.309, model sonnet. Cost $0.11, 5 turns.

Question: which weeks of this course talk about testing whether an AI feature works?

---

Weeks 12 and 13 are the two that test whether an AI feature works. Weeks 9 to 11 only test the plumbing, and week 1 only points ahead to week 12.

## Main weeks

**Week 12, Evaluation** is the core one.
- `12-evaluation/README.md:3`: the goal is to find out how well your AI feature really works, with evidence instead of impressions.
- `12-evaluation/README.md:50-52`: an evaluation has four parts, starting with a fixed test set that includes hard cases.
- `12-evaluation/README.md:73-81`: the deal screener's 20-case evaluation, with the scoring rule committed before any run.
- `12-evaluation/README.md:103`: the same listing got two different answers in two runs, which is why one good run proves little.
- `12-evaluation/README.md:107`: you build your own 20-case test set, with 5 cases held out.
- `12-evaluation/README.md:154`: you write the script that scores your feature.
- `12-evaluation/slides.md:43-45`: the same four parts of an evaluation.
- `12-evaluation/slides.md:149`: never change the test set to raise the score.
- `12-evaluation/assignment.md:7-9`: the test set must be committed before the script.

**Week 13, Security and responsible use** tests whether the feature holds up against hostile input.
- `13-security-and-responsible-use/README.md:102`: the deal screener's injection test uses 8 hostile listings.
- `13-security-and-responsible-use/README.md:115`: the command is `python3 -m dealscreener.evaluate --injection`.
- `13-security-and-responsible-use/README.md:98`: the advice to red-team your own agent by testing it with deliberately injected documents and emails.
- `13-security-and-responsible-use/README.md:166-174`: you run your own evaluation with `--injection` before and after a defence, then re-run the normal cases to check the defence didn't break them.

## Weeks that only touch on it
- **Week 1** (`01-what-is-ai/slides.md:241`, `01-what-is-ai/README.md:131`): says you can't take a model's word for it and points ahead to week 12 to measure how often it is right.
- **Week 9** (`09-calling-a-model/README.md:277`): quotes Anthropic's advice to test your use case and evaluate whether performance meets your requirements before upgrading models. Its other test material is offline tests with a fake model (`09-calling-a-model/slides.md:260`, `09-calling-a-model/README.md:406`). Those test the code, not whether the AI answers well.
- **Week 10** (`10-embeddings-and-rag/assignment.md:10`) and **week 11** (`11-tools-agents-mcp/assignment.md:11`): also fake-model offline tests only.
- **Week 11** (`11-tools-agents-mcp/README.md:186`): a short note to test your prompt with real runs and read the answers.
- **Week 14** (`14-final-demos/assignment.md:13`): checks that your week 12 evaluation and week 13 injection results are committed.

## Search commands used
1. Glob with pattern `**/*` in `weeks`. This listed all the files.
2. Grep in `weeks`, case-insensitive, `output_mode: count`. The pattern was `\b(evals?|evaluat\w*|test(s|ing)?|benchmark\w*|regression|golden set|LLM-as-judge|assert\w*)\b`. It was too broad, with 540 hits mostly about code tests.
3. Grep in `weeks`, `glob: *.md`, case-insensitive, `output_mode: content`, `head_limit: 0`. The pattern was `\b(evals?|evaluat\w*|golden set|test set|LLM-as-judge|judge|rubric|accuracy|hallucinat\w*|regression)\b`. This produced the main results.
4. Grep in `weeks`, `glob: {09,10,11,13,01}*/*.md`, case-insensitive, `head_limit: 40`. The pattern was `fake model|offline test|test(s|ed|ing)? (the|your|whether)|check(ing)? (that|whether|if) .*(answer|right|correct|work)|how often`. This separated plumbing tests from answer-quality testing.

I read results from grep output and did not open whole files. Several long lines, such as `12-evaluation/README.md:59`, were omitted by the grep display, so I haven't read them. I also didn't read the `.pdf` slides, which are copies of the `slides.md` files.
