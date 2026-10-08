# wordstats - plan

A small command-line tool that reports word statistics for text files.
Python 3.10+, standard library only. Tests use `unittest`:

```bash
python3 -m unittest discover -s tests
```

Every task below must come with at least one test, and all tests must pass
before the task counts as done.

## Design

- Entry point: `python3 -m wordstats FILE [FILE ...] [options]`
- A word is a run of letters, digits or apostrophes. Matching is
  case-insensitive (`The` and `the` are the same word).
- Code lives in `wordstats/`. One module per concern is fine
  (`cli.py`, `words.py`, `stats.py`, `output.py`). Do not name a module
  `tokenize.py`: it shadows the standard library module of the same name.

## Tasks

Dependencies are listed as task numbers. A task can start once everything
it depends on is done.

| # | Task | Depends on |
|---|------|------------|
| 1 | CLI skeleton: `python3 -m wordstats FILE` parses arguments with argparse and exits 0 | - |
| 2 | Read a file as UTF-8, replacing undecodable bytes instead of crashing; a missing file prints an error and exits 2 | 1 |
| 3 | Tokenizer: turn text into a list of lowercase words using the rule in Design | - |
| 4 | Basic counts: lines, words, characters for one file, printed one per line | 2, 3 |
| 5 | `--top N`: the N most common words with their counts, ties broken alphabetically | 4 |
| 6 | `--no-stopwords`: drop common English stopwords (keep the list in `wordstats/stopwords.py`) before counting | 3 |
| 7 | Table output (the default): counts as an aligned two-column table | 4 |
| 8 | `--json`: the same results as a JSON object instead of a table | 4 |
| 9 | Several files: one table section per file plus a `TOTAL` section | 7 |
| 10 | Stdin: `-` as a file name reads standard input | 2 |
| 11 | `--min-length N`: ignore words shorter than N characters | 3 |
| 12 | README with usage examples for every option above | 5, 6, 8, 9, 10, 11 |
