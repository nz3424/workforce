# CLAUDE.md — Nick Zhu's Master Context File

> **All agents: read this file before every task.** This is the shared identity
> and preference layer for the entire workforce. Do not skip it.

---

## Identity

- **Name:** Nick Zhu
- **Email:** nicholaszhu14@gmail.com
- **Status:** Recent college graduate, transitioning into a full-time Software
  Engineering role (as of May 2026)
- **Location:** TBD — update once settled after graduation

---

## Current Goals & Priorities

These are in priority order. When in doubt about what matters, refer here.

1. **Land strong at my new job** — ramp up fast on the codebase, make a strong
   early impression, ask good questions, ship early wins
2. **Stay organized** — keep tasks tracked, don't drop balls, do a weekly
   review every Sunday to prepare for the week ahead
3. **Ship side projects** — keep building personal/portfolio work in evenings
   and weekends; this is important for long-term growth
4. **Build long-term career capital** — network intentionally, learn in public
   (writing, GitHub, etc.), develop a clear area of technical expertise

---

## Communication Style

### Email tone
- **Default:** Friendly and direct — warm but concise, gets to the point
  without being stiff or overly formal
- **With managers / senior people:** Confident and professional, but never
  stiff; no unnecessary padding
- **With peers / friends:** Casual and conversational
- **With recruiters / external contacts:** Polished, enthusiastic, brief
- **Sign-off (professional):** "Best, Nick"
- **Sign-off (casual):** "Thanks, Nick" or just "Nick"

### General writing principles
- Lead with the point, then context — don't bury the ask
- Short paragraphs; no walls of text
- Never use filler phrases like "I hope this email finds you well"
- Prefer concrete language over vague qualifiers

---

## Work Style

- **Style:** Flexible and adaptive — no rigid daily structure; goes with what
  is most needed each day
- **Deep work:** Protect mornings when possible for complex, high-focus tasks
- **Task format:** Concise action items I can scan quickly; spare me lengthy
  preambles
- **Decisions:** Give me options with tradeoffs, not just one answer — I like
  to make the final call with full context
- **Output length:** Default to short. Put detail in appendices or follow-ups
  if needed.

---

## Technical Preferences

- **Field:** Software Engineering
- **Code style:** Clean and readable; comment complex logic, but don't
  over-comment obvious things; no over-engineering
- **Testing:** Always suggest or include tests for any non-trivial code
- **Commits:** Small, focused commits with clear imperative messages
  (e.g. "Add auth middleware" not "changes")
- **PRs:** Prefer small focused PRs; include a short description of what
  changed and why
- **Code reviews:** Explain the *why* behind feedback, not just the *what*
- **Languages & stack:** Update `preferences.md` once settled at new job

---

## Agent Instructions

These rules apply to every agent in the workforce.

| Rule | Detail |
|---|---|
| **Read this file first** | Always load CLAUDE.md before starting any task |
| **Read your memory file** | Load your agent memory file before starting (see Memory Convention below) |
| **Draft, don't send** | All emails go to `Communication Team/drafts/` for Nick's review |
| **Propose, don't act** | For calendar changes, suggest before writing anything |
| **Be concise** | Default to short outputs; Nick can ask for more |
| **Surface tradeoffs** | Present options when making decisions, not just one path |
| **Update memory** | After any session, append new learnings to your agent memory file |
| **Check contacts** | Before drafting any email, read `contacts.md` for tone guidance |

---

## Memory Convention

Every agent in the workforce has two levels of memory:

| Level | File | Scope |
|---|---|---|
| **Workforce-wide** | `HQ/memory.md` | Active projects, open threads, major decisions — shared across all agents |
| **Agent-specific** | `[Team]/agents/memory/[agent-name].md` | Learnings, preferences, and run logs specific to that agent |

### File location pattern

```
[Team Name]/
└── agents/
    ├── [agent-name].md        ← agent spec
    └── memory/
        └── [agent-name].md   ← agent memory
```

### Rules for agent memory files

- **Read on startup** — load your memory file right after `HQ/CLAUDE.md`
- **Append, never overwrite** — add new entries below existing ones; date every entry
- **Promote to contacts.md** — if a per-recipient pattern repeats 2–3 times, move it to `HQ/contacts.md`
- **Promote to HQ/memory.md** — if a learning is relevant to all agents, add it there instead
- **Keep it short** — one line per entry where possible; this file should stay scannable

---

## Key HQ Files

| File | Purpose |
|---|---|
| `memory.md` | Live context: current projects, recent decisions, ongoing threads |
| `contacts.md` | Key people and how to communicate with each |
| `preferences.md` | Formatting defaults, code style details, output structure |

---

*Last updated: May 2026 — update this file whenever your goals, stack, or
situation changes significantly.*
