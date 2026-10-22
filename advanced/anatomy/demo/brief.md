# Brief: how a Claude Code skill gets used

This is the true behaviour the figure has to explain. Every number on the
figure (readout, caption, part counts) must come from these facts.

## The idea

Claude Code does not read every skill in full at the start of a session.
It works in three steps, often called "progressive disclosure":

1. **At startup** it reads only the short `name` and `description` from the
   top of each installed `SKILL.md` (one short paragraph each). That is all
   that sits in Claude's memory for each skill until it is needed.
2. **When a request matches a description** (or you type `/skill-name`),
   Claude opens that one skill and reads the whole `SKILL.md` body.
3. **Only if the body points to them**, Claude opens the extra files in the
   skill's folder (references, scripts, examples) one at a time, as needed.

So 7 installed skills cost about 7 short descriptions of memory, not
7 whole manuals, and a skill's long reference files cost nothing until a
task actually needs them.

## Numbers to use

- Skills installed in this demo: **7** (one is the one being used).
- Skills opened for this request: **1**.
- Each description: at most **1,024 characters**.
- The `SKILL.md` body Claude reads on a match: about **185 lines** for this
  very skill (Anatomy).
- Extra files that skill can open on demand: **10** reference guides.

## What should move

A request comes in. Claude checks it against the 7 short descriptions,
picks the one that matches, pulls that skill's full instructions out, and
only then reaches for one of its reference files. The live readout shows
which stage it is at and how much has been loaded so far.
