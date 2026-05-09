# /log — Session Log

Record what happened this session in `HQ/session-log.md`. Follow these steps exactly.

## Step 1 — Reflect on the session

Look back at this conversation and identify:
- **What was worked on:** 1–3 bullet points, concrete and specific (e.g. "Built /log skill", "Debugged morning-briefing agent output format")
- **Agents or skills used:** List any agents invoked or skills run (e.g. researcher, email-drafter, /sync, /research-paper). If none, write "None — direct Claude session"
- **What worked well:** One sentence on something that felt productive or clicked
- **What to improve:** One sentence on friction, confusion, or something worth changing

Keep each field short — this log should stay scannable.

## Step 2 — Read the log file

Read `HQ/session-log.md`. If it doesn't exist, create it with this header:

```
# Session Log

> One entry per session. Append only — never edit past entries.
> Run /log at the end of any meaningful Claude session.

---
```

Count the number of existing `## ` entries to determine the session number.

## Step 3 — Append the new entry

Append this block at the bottom of `HQ/session-log.md`:

```
## [YYYY-MM-DD] — [3–5 word title describing what this session was about]

- **Worked on:** [bullet 1]; [bullet 2]; [bullet 3 if needed]
- **Agents/skills used:** [list, or "None — direct Claude session"]
- **What worked:** [one sentence]
- **What to improve:** [one sentence]

---
```

Use today's date. The title should be a short phrase that would let Nick scan the log and know what happened (e.g. "Built session log skill", "Debugged briefing agent", "Research paper on LLMs").

## Step 4 — Insights pass (every 5 sessions)

If the new entry is the 5th, 10th, 15th, etc. (i.e. session count is a multiple of 5):

Read the full log and surface a short insights block **after** writing the entry:

```
---
### Patterns from last 5 sessions

- **Most used agents/skills:** [list with rough counts]
- **Recurring friction:** [anything that shows up as "what to improve" more than once]
- **What's working:** [any consistent themes in "what worked"]
- **Workforce suggestion:** [one concrete thing to add, change, or retire based on usage patterns]
---
```

Print this to the conversation so Nick sees it. Do not write it to the log file.

## Step 5 — Confirm

Report: "Logged. Session #[N] added to HQ/session-log.md."

Do not push or sync — let Nick run /sync when ready.
