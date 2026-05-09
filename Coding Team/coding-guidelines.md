# Coding Guidelines

Behavioral standards for all Coding Team agents. Read this after `HQ/CLAUDE.md`
and before starting any task.

---

## Think Before Coding

State your assumptions explicitly before writing anything. If a task has multiple
valid interpretations, surface them — don't pick one silently. If something is
unclear or seems wrong, stop and ask rather than guessing.

- Ambiguity surfaced before coding is cheap. Ambiguity discovered after is expensive.
- If a simpler approach exists, say so and get confirmation before proceeding with
  the more complex one.

---

## Read Before Writing

Before adding or changing code, read the relevant exports, immediate callers, and
shared utilities — not just the file being edited.

- "Looks orthogonal" is dangerous. Code that appears isolated often has hidden
  coupling.
- If you don't understand why code is structured a certain way, ask rather than
  assuming it's arbitrary.

---

## Tests Verify Intent, Not Just Behavior

A test must encode *why* the behavior matters, not just *what* it does. A test
that would still pass after a business logic change is wrong — it's verifying
implementation, not intent.

- Name tests after the scenario and expected outcome, not the function under test.
- A failing test on a valid refactor means the test was wrong, not the refactor.

---

## Surface Conflicts, Don't Average Them

If two patterns in the codebase contradict each other, pick the more recent or
more thoroughly tested one. Explain the choice. Flag the other pattern for
cleanup. Do not blend the two.

- Blended patterns compound over time and become harder to untangle than the
  original conflict.
- "I followed the pattern in file X" is not a defense if file X contradicts
  file Y — that conflict should have been flagged.

---

## Match the Codebase's Conventions

Conform to the existing codebase style, even when you'd do it differently. The
goal is a consistent codebase, not a personally optimal one.

- If you genuinely believe a convention is harmful, surface it explicitly and let
  Nick decide. Do not silently fork to a different style.
- Consistency > taste when working inside an existing codebase.

---

## Checkpoint After Every Significant Step

After each meaningful unit of work, summarize: what was done, what was verified,
what remains. Don't proceed from a state you can't clearly describe.

- If you lose track of where you are, stop and restate the state before continuing.
- A checkpoint is especially important before any destructive or hard-to-reverse
  operation.

---

## Fail Loud

"Completed" is wrong if anything was skipped silently. "Tests pass" is wrong if
any tests were skipped or excluded. Surface uncertainty — don't hide it behind
success language.

- If something was not done or not verified, say so explicitly.
- A partial result labeled as complete is worse than an honest incomplete.

---

## Goal-Driven Execution (Code Writer)

*Primarily applies to Code Writer for multi-step implementation tasks.*

Before starting a non-trivial task, define what "done" looks like in verifiable
terms. For each step, state the check that confirms it succeeded:

```
1. [Step] → verify: [command or test]
2. [Step] → verify: [command or test]
```

Strong success criteria let you loop to completion independently. Weak criteria
("make it work") require constant clarification.
