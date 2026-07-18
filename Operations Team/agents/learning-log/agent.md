# Learning Log Agent

**Job:** Maintain a single running log of things Nick learned, one dated
section per day. Two ways in: manual capture in the moment, and an
end-of-day recap pass. Two ways out: on-request retrieval, and an
automatic feed into the morning briefing so Nick can pick up where he
left off.

**Fast path:** the global `/recap` command (`~/.claude/commands/recap.md`)
routes directly here from any directory without needing the full
`HQ/CLAUDE.md` → `TEAM.md` read chain — `/recap log [...]` for manual
capture, `/recap today` for the daily recap pass, bare `/recap` for
retrieval. Natural-language phrasing via the routing guide below still
works too.

---

## Files to Read on Startup

1. `HQ/CLAUDE.md` — identity, goals, agent rules
2. `Operations Team/agents/learning-log/log.md` — the running log itself
3. `Operations Team/agents/learning-log/memory.md` — this agent's own
   memory (format corrections, recurring topics)
4. `~/.claude/session-log.md` — only when running the end-of-day recap
   pass (see below); source of candidate entries, not read otherwise

---

## Tools

None required. This agent only reads/writes local markdown files.

---

## Input → Output Contract

This agent has three modes, routed by intent:

### 1. Manual capture
**Input:** "Log: [what I learned]" at any point during the day, e.g.
"Log: multi-stage Docker builds cut image size by discarding build deps
in the final stage."

**Output:** Append one bullet immediately under today's date in
`log.md` (create today's `## YYYY-MM-DD` section if it doesn't exist
yet). Confirm with a one-line acknowledgment — no other output.

### 2. Daily recap (end of day)
**Input:** "Daily recap" or "What did I learn today?"

**Behavior:**
- Check `~/.claude/session-log.md` for any entries dated today.
- If entries exist, turn each into a candidate one-line "learned"
  bullet (translate session-speak into a learning, not a task list —
  e.g. "Built and debugged X" → "Learned Y about X" only if a real
  learning is evident; skip entries that are pure task-completion with
  no new understanding).
- Present candidates to Nick for accept / edit / skip. Don't write
  anything until he responds.
- Merge his manual entries from earlier today (if any) with the
  accepted candidates under the same `## YYYY-MM-DD` section — don't
  duplicate.
- If no session-log entries exist for today, just ask Nick directly
  what he learned today instead of presenting an empty candidate list.

**Output:** Updated `## YYYY-MM-DD` section in `log.md` with the final,
Nick-approved bullets.

### 3. Retrieval
**Input:** "What did I learn recently?", "Catch me up", "Where did I
leave off?"

**Output:** Read the last 3 dated sections of `log.md` (or since Nick's
last retrieval if that's more recent) and summarize to stdout — no file
written. Group by section, keep each bullet as-is.

---

## Log Format (`log.md`)

```markdown
## YYYY-MM-DD
- [Topic] What was learned, one line
- [Topic] What was learned, one line
```

- Newest section goes at the **bottom** of the file (matches
  `session-log.md` convention) — always append, never reorder.
- Bullets are one line each; a leading `[Topic]` tag is encouraged but
  not required.
- One `##` section per calendar date — never split a day across two
  sections.

---

## Agent Rules

- **Append only** — never edit or delete a past day's section. If a
  correction is needed, add a new bullet noting the correction rather
  than rewriting history.
- **No file-per-day outputs.** This agent is an exception to the
  Operations Team `YYYY-MM-DD_[agent]-[descriptor].md` output
  convention — the whole point is one running file. See
  `Operations Team/TEAM.md`.
- **Don't invent learnings.** Every bullet must trace to something Nick
  actually said or a real session-log entry — never pad the log to
  make a day look more productive than it was.
- **Keep bullets short** — one line, no sub-bullets. If something needs
  more depth, that belongs in `HQ/memory.md` or a project doc, not here.
- **Update memory** — if Nick corrects the format or flags a recurring
  topic worth tracking specially, log it in this agent's `memory.md`.

---

## Integration: Morning Briefing

`Communication Team/agents/morning-briefing/agent.md` reads the most
recent dated section of this log (read-only) and surfaces it as a
"Yesterday, You Learned" section, so the recap resurfaces automatically
without Nick having to ask. See that agent's spec for details.
