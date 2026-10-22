# Claude Code + xerj MCP

Captured 2026-10-22 with xerj v1.0.0-rc.98, Claude Code 2.1.309, model sonnet. Cost $0.15, 6 turns.

Question: which weeks of this course talk about testing whether an AI feature works?

---

## Weeks that cover testing whether an AI feature works

**Week 12: Evaluation** is the main one.
- It covers building an evaluation: a fixed test set, expected answers written before any run, a scoring rule, and a score plus a list of misses. `12-evaluation/README.md:48`
- It explains why "it looked right" isn't evidence, and sets the honesty rules: write the answers first, never edit the test set to raise the score, and hold out 5 cases. `12-evaluation/README.md:20`
- It says 20 cases can show patterns of misses but not a precise rate, because one case is 5% of the score. `12-evaluation/README.md:48`, and slide page 8 of `12-evaluation/slides.pdf`.
- It walks through the deal screener's 20-case evaluation. Running it twice gave different answers on the same listing, and a perfect dev score may mean the set is too easy. `12-evaluation/README.md:73` and `:103`
- Students build their own 20-case set (step 4 onward). `12-evaluation/README.md:103`
- The run protocol is two dev runs, reading every miss, making one change, then one held-out run. `12-evaluation/README.md:166`
- The assignment rubric grades the test set, an offline-tested evaluation script, and a report on what the score does and doesn't show. `12-evaluation/assignment.md:19`

**Week 9: Calling a model from code** covers this only indirectly.
- It covers automated tests that use a fake model and pass with no key, including a test for "no key". `09-calling-a-model/README.md:384` and `09-calling-a-model/assignment.md:1`
- The assignment also asks how you made answers dependable and what your code checks before using an answer. `09-calling-a-model/assignment.md:1`

**Week 10: Embeddings and RAG** is a secondary mention.
- Its tests use a fake embedder and a fake model, plus one live test run only with `RUN_LIVE_TESTS=1`. This is on page 15 of `10-embeddings-and-rag/slides.pdf`. `10-embeddings-and-rag/assignment.md:1` covers the same requirement.
- The assignment also asks for a question your documents can't answer, to check that the program says so. `10-embeddings-and-rag/assignment.md:1`

**Week 11: Tools, agents and MCP** is a minor mention.
- Its tests include a fake model asking for the tool and one that hits the 5-turn limit. `11-tools-agents-mcp/README.md:281`

Week 12 is the only week about testing whether an AI feature works. Weeks 9 to 11 test the code with fakes rather than judging the model's answers. I did not find any other week on this topic, but my searches were not exhaustive.

## xerj tool calls

1. `xerj_map` with no arguments. It showed one index, `course-docs`.
2. `xerj_search` with `index: "course-docs"`, `query: "evaluating testing whether an AI feature works evals"`, `size: 10`, `max_tokens: 3000`
3. `xerj_search` with `index: "course-docs"`, `query: "week test quality LLM judge golden set regression"`, `size: 10`, `max_tokens: 3000`
4. `xerj_search` with `index: "course-docs"`, `query: "automated tests pass fake model check answer correct"`, `size: 8`, `max_tokens: 2500`, `_source: ["title","ax_path","start_line","page"]`

I also ran one `ToolSearch` call to load the xerj tool schemas. It isn't a xerj tool.

Line numbers are the `start_line` of the matched passage, so the cited text begins at or just after that line.
