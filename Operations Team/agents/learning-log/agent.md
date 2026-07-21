# Learning Log Agent

**Job:** Maintain a single running log of things Nick learned, one dated
section per day. Two ways in: manual capture in the moment, and an
end-of-day recap pass — run either interactively or unattended by a
nightly scheduled job. Two ways out: on-request retrieval, and an
automatic feed into the morning briefing so Nick can pick up where he
left off.

**Fast path:** the global `/recap` command (`~/.claude/commands/recap.md`)
routes directly here from any directory without needing the full
`HQ/CLAUDE.md` → `TEAM.md` read chain — `/recap log [...]` for manual
capture, `/recap today` for the daily recap pass, `/recap auto` for the
unattended nightly pass (scheduled job only), bare `/recap` for
retrieval. Natural-language phrasing via the routing guide below still
works too.

---

## Files to Read on Startup

1. `HQ/CLAUDE.md` — identity, goals, agent rules
2. `Operations Team/agents/learning-log/log.md` — the running log itself
3. `Operations Team/agents/learning-log/memory.md` — this agent's own
   memory (format corrections, recurring topics)
4. `~/.claude/session-log.md` — only when running the Daily recap or
   Automated recap pass (see below); source of candidate entries, not
   read otherwise
5. Output of `Operations Team/agents/learning-log/extract_transcripts.py`
   — only during the Daily recap or Automated recap pass; today's raw
   Claude Code session transcripts across every project, not just
   Workforce

---

## Tools

None required. This agent only reads/writes local markdown files.

---

## Input → Output Contract

This agent has four modes, routed by intent:

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
- Check today's `## YYYY-MM-DD` section in `log.md` for a
  `<!-- last-recap-pass: TIMESTAMP -->` watermark comment (see
  "Watermark" below). If present, only consider session-log entries and
  transcript activity **after** that timestamp; if absent, process the
  whole day.
- Check `~/.claude/session-log.md` for any entries dated today (after
  the watermark, if one exists).
- Run `python3 "Operations Team/agents/learning-log/extract_transcripts.py"`
  (no argument = today, local time) to pull today's raw Claude Code
  session transcripts across **every** project — not just Workforce.
  It strips tool_use/tool_result/thinking noise down to just the
  user/assistant text exchanges, grouped by project and session.
  Discard any transcript activity before the watermark.
- From both sources, draft candidate one-line "learned" bullets —
  translate session-speak into a real learning, not a task list (e.g.
  "Built and debugged X" → "Learned Y about X" only if a genuine
  learning is evident; skip entries that are pure task-completion or
  small talk with no new understanding). Tag each candidate with its
  source project when it isn't Workforce, e.g. `[llm-training] ...`.
- If the same learning shows up in both session-log.md and a
  transcript, propose it once.
- Present candidates to Nick for accept / edit / skip. Don't write
  anything until he responds.
- Merge his manual entries from earlier today (if any) with the
  accepted candidates under the same `## YYYY-MM-DD` section — don't
  duplicate.
- If neither source has anything new since the watermark, just ask Nick
  directly what he learned today instead of presenting an empty
  candidate list.
- Transcripts can be long even after stripping tool noise — if a
  day's output from the script is large, prioritize sessions that read
  as substantive/explanatory over short or purely operational ones
  rather than reading everything in exhaustive depth.
- After writing, update the watermark (see below).

**Output:** Updated `## YYYY-MM-DD` section in `log.md` with the final,
Nick-approved bullets.

### 3. Automated recap (unattended, nightly)
**Input:** Fired only by the scheduled `com.nickzhu.claude-recap` launchd
job via `/recap auto YYYY-MM-DD`, at 11:55 PM local time. Not intended for
manual use — no one is present to respond to prompts. The wrapper script
(`~/.claude/scripts/run-recap-auto.sh`) captures the target date once,
atomically, at invocation and passes it in the command.

**The passed date is authoritative — never re-derive "today" from your own
clock in this mode.** The job fires at 23:55 and a run can drift past
midnight; by the time you write, your injected `currentDate` context and
`datetime.now()` may already read the *next* day. The wrapper captures the
date once, atomically, at invocation, so the passed `YYYY-MM-DD` is the
**upper bound** of what this run should cover. (If, exceptionally, no date
is passed, fall back to local today as the upper bound.)

**Catch up on every un-recapped day, not just the upper-bound date.**
launchd does not reliably run a missed nightly fire: if the Mac was powered
off at 23:55 that night is skipped outright, and if it was asleep the job
runs on wake with a *later* date — either way, days silently fall through
the cracks. So this pass is responsible for the whole backlog since the log
was last touched, healing those gaps retroactively:

1. Find the **most recent watermark** anywhere in `log.md` — the last
   `<!-- last-recap-pass: YYYY-MM-DDThh:mm:ss -->` comment (it lives at the
   end of the newest recapped section). Its date is `last_recap_date`. If
   the log has no watermark at all, treat `last_recap_date` as the
   upper-bound date (nothing to back-fill — first run).
2. Build the list of calendar dates to process: **every date from
   `last_recap_date` through the upper-bound date, inclusive.** In the
   common case (job ran last night as normal) this is just one or two days;
   after an outage it may be several.
3. Process each date in the list in ascending order (see Behavior below).
   For `last_recap_date` itself, honor its existing same-day watermark —
   only consider activity *after* that timestamp (usually nothing, which is
   fine). Every later date has no watermark yet, so process its whole day.

**Transcripts are the primary source of truth.** `session-log.md` is a
supplementary convenience capture — Nick often does a substantial day of
work and never `/log`s any of it, so an empty or sparse session-log is
normal and must NOT short-circuit the pass. For each date being processed,
always run `extract_transcripts.py <that-date>` regardless of session-log
state, and treat the transcripts as the main well to draw candidates from;
fold in any session-log entries on top, deduped.

**Behavior (per date in the catch-up list):** Identical candidate-sourcing
as Daily recap — same watermark check, same `session-log.md` +
`extract_transcripts.py <date>` sourcing, same filtering rules (translate
session-speak into a real learning, skip pure task-completion, tag
non-Workforce candidates by project, dedupe overlap between the two
sources) — with one difference:
- **Skip the review gate.** Do not present candidates or wait for a
  response. Every candidate that passes the existing filters is
  appended directly to that date's `## YYYY-MM-DD` section.
- Create each date's section if it doesn't exist, or merge into it
  (without duplicating) if manual entries were already logged that day.
  Keep sections in ascending date order, newest at the bottom — since
  every caught-up date is newer than the last existing section, plain
  append preserves order; never reorder or edit an earlier day's bullets.
- If a given date has zero qualifying candidates, do nothing for that
  date — don't create an empty section, don't invent filler content,
  don't write or advance its watermark. Move on to the next date.
- After writing a date's bullets, stamp that date's watermark (see below).
- Still bound by all the Agent Rules below (append-only, never invent,
  keep bullets short) — the only behavioral difference from Daily recap
  is skipping accept/edit/skip.
- Confirmation goes to stdout, which lands in
  `~/.claude/logs/recap-cron.log` — no one reads it live, so keep it
  short; note how many days were caught up if more than one.

**Output:** One updated/created `## YYYY-MM-DD` section per caught-up date
in `log.md`, written without human review.

### Watermark (Daily recap and Automated recap only)
Serves two jobs. **Within a day:** prevents duplicate or resurrected
candidates when recap runs more than once (e.g. a manual `/recap today` at
5 PM followed by the 11:55 PM automated pass) — without it, a later pass
would re-derive candidates from the *whole* day, re-proposing bullets
already written and silently writing anything explicitly skipped earlier
(nothing records a skip otherwise). **Across days:** the most recent
watermark in the file is the automated pass's low-water mark for catch-up
(see Automated recap step 1) — it marks the last day that was recapped, so
the next run knows exactly how far back the backlog reaches.

- After a recap pass finishes writing a given date's bullets, append an
  HTML comment at the end of **that date's** section:
  `<!-- last-recap-pass: 2026-07-19T17:03:00 -->` (local time, invisible
  in normal reads, not counted as a bullet). If a watermark comment
  already exists for that date, replace it rather than adding a second one.
  In a multi-day catch-up run, each processed date gets its own watermark.
- Within a date, each pass only derives candidates from activity **after**
  that date's existing watermark timestamp — not the whole day.
- If no pass has run yet for a date (no watermark in its section), treat it
  as start-of-day and process the whole day.
- A pass that finds zero qualifying candidates for a date does not write or
  advance that date's watermark — nothing changed, so there's nothing new
  to bound, and the catch-up low-water mark stays where it was.

### 4. Retrieval
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
  actually said, a real session-log entry, or a real transcript
  exchange — never pad the log to make a day look more productive than
  it was.
- **Transcripts are read-only.** `extract_transcripts.py` only reads
  `~/.claude/projects/**/*.jsonl` — never write to, move, or delete a
  transcript file.
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
