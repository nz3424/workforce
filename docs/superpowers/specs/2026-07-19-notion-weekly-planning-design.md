# Notion Weekly/Daily Planning System — Design

*Date: 2026-07-19*
*Status: Approved by Nick, pending implementation plan*

## Problem

Nick has no structured place in Notion for weekly/daily task planning. His only
existing Notion task surface, **Nick's Tasks Tracker**, is a flat database good
for structured project-level items but not for day-to-day execution planning
(no daily granularity, no backlog, no categories). Two existing agents
(`task-planner`, `weekly-review`) partially cover this today but require Nick
to remember to invoke them, and don't rank or prioritize across projects — he
has to manually decide what's worth working on each day.

Goals:
1. A durable Notion structure for weekly/daily planning — a backlog plus
   per-day category checklists — inspired by
   `github.com/CameronCrow/workforce/tree/main/agents/time-management` (its
   `daily-planner` skill and `time-management-director` agent in particular).
2. A single agent that both takes direct requests ("plan my week," "plan my
   day," "I have to do X, Y, Z today") and runs autonomously on a schedule, so
   Nick doesn't have to remember to invoke it.
3. Continuous, autonomous prioritization across all of Nick's projects — the
   system decides what's worth working on next, rather than Nick manually
   curating a queue every day — while keeping any real-world side effects
   (not just list-making) behind an explicit approval gate.

## Reference research

Investigated the linked repo in detail (not just skimmed): `todo-manager`
(deprecated 2026-07-13, replaced for the reason below), `time-management-director`
(routes cross-system vs. single-system requests between `calendar-manager` and
`daily-planner`), `skills/daily-planner/` (the current weekly-page system and
its Notion schema), `planning/notion-todo-overhaul.md` (why they moved off a
single evergreen page), and `planning/auto-goal-setting.md` (an explicit,
unimplemented brief for exactly the "no human-in-the-loop prioritization"
problem this design also tackles — flagged here because it's evidence this is
a genuinely unsolved, harder problem, not a small extension).

Key lessons pulled from that research and applied below:
- **Single evergreen page, rebuilt each morning, silently loses data.**
  Cameron's repo hit this directly: `update_content` failures went unnoticed
  mid-rebuild, and pre-seeded future days got erased. Fixed by moving to one
  durable page per week, written additively, never rebuilt from scratch.
- **HAL orchestrator** (their closest working analog to autonomy) stays
  approval-gated: it proposes a ranked plan read-only, requires one explicit
  approval, then executes. It never removes the human checkpoint before
  anything with a real effect happens — informs the execution-gate design
  below.
- Confirmed live against Cameron's actual current-week page (shared with Nick
  as guest access) that the structural pattern described in this doc — backlog
  + per-day category checklists + a markdown link to a separate structured
  tasks DB — matches what's actually in production use, not just documented
  aspirationally.

## Notion structure

### Weekly Pages database (new)

- One row = one week. Title: `"Week of <Mon Date> (YYYY-Www)"`.
- Properties — kept minimal on purpose (Cameron's page carries `Category`,
  `Est. Time (hrs)`, `Notes`, `Priority`, `Status` properties at the page
  level that are empty on every single row in production; not worth copying
  dead schema):
  - `Due Date` — date range, Monday → Sunday. This is the lookup key: "current
    week" = the row whose range contains today, matched client-side (do not
    rely on server-side filtering — tier-dependent and unreliable per the
    reference repo's notes).
  - `Calendar Synced` — checkbox, reserved for future calendar-integration use.
- **Rollover**: triggered when no row covers today. Create a new page for the
  upcoming week; carry the Backlog section forward verbatim; flag any Backlog
  item that has now survived 3+ rollovers for an explicit keep/drop decision
  in the next digest, rather than either silently dropping it or letting it
  persist forever unexamined.
- **Additive, not destructive**: a `### <Weekday>` section is written once and
  persists. The planning agent merges new items in; it never regenerates a
  day's section from scratch. This is the fix for the exact failure mode the
  reference repo documented.

### Weekly page template

```markdown
## Backlog
- [ ] <item>              (loosely grouped by category; no rigid tags)

### Monday
- [ ] Deep Work
   - [ ] Fix ternary quant bug [BitNet]
- [ ] Job Prep
- [ ] Personal
- [ ] Fitness
- [ ] Chores

### Tuesday – Sunday
[same category skeleton]

[Open Nick's Tasks Tracker →](<link>)
```

- **Categories**: `Deep Work`, `Job Prep`, `Personal`, `Fitness`, `Chores`.
  Chosen as a hybrid — categories stay simple and scannable, but items under
  `Deep Work` carry an inline project tag (`[BitNet]`, `[Coding]`,
  `[Research]`, `[Side: X]`) so the ranking engine can still reason per-project
  underneath a clean surface. Category skeleton is a default frame, not
  mandatory — atypical days can deviate.
- Multi-step items get nested sub-bullets underneath a parent line.
- Freeform inline notes are allowed directly in the checklist (e.g. a
  `NOTE:` line flagging something as blocked) — this stays markdown, never a
  structured form.
- Checkboxes: `- [ ]` open, `- [x]` done. "Checking a box is done" is the
  ground truth signal for passive completion detection (see below).
- Bottom-of-page link to Nick's Tasks Tracker is a plain markdown link, not a
  live embed — Notion's API doesn't support reliable inline database embeds
  (confirmed pitfall from the reference repo; do not attempt it).

### Relationship to Nick's Tasks Tracker (existing database)

- Tasks Tracker is the system of record for **structured, multi-day work**:
  anything worth tracking over time with its own due date/priority/status.
  This is the "major tasks" Nick referred to.
- Personal one-offs, chores, and single-day items never get a Tasks Tracker
  row — they live only on the weekly page.
- `Deep Work` checklist items on a given day are short imperative restatements
  of open Tasks Tracker rows the ranking engine selected for that day, tagged
  with the project label.
- **Schema fix required**: the live Tasks Tracker has drifted from its
  documented spec (`Operations Team/agents/task-planner/agent.md`) — it
  currently has `Task type` (Bug/Feature/Polish) and `Effort level`, leftover
  from Notion's default template, instead of `Project/Area`, `Source`,
  `Notes`, `Agent Tag`. The new agent needs `Project/Area` and a reliable
  `Priority` field to rank against, so this schema needs correcting as part of
  implementation — call this out explicitly in the implementation plan.

## Agent architecture

**One new agent** (working name: `planning-director` — easy to rename) fully
replaces `task-planner` and `weekly-review`. It does not call either as a
dependency — it implements what it needs directly (Notion read/write, Gmail,
Drive, Calendar, Canvas-sweep-output reads). This was an explicit choice over
building a thin orchestrator on top of the old agents, since both are
considered deprecated in function, not just in name.

- `task-planner` and `weekly-review` folders get **archived, not deleted** —
  their memory files (notably the Tasks Tracker database ID and Notion user
  ID already resolved in `task-planner/memory.md`) get carried into the new
  agent's memory so it doesn't need to re-bootstrap.
- `standup-prep` is untouched — different purpose (job standup format, not
  personal task management), out of scope here.
- `canvas-sweep` is untouched and continues to feed candidate tasks the same
  way it does today.
- **Direct invocation** (unchanged trigger phrases from `task-planner` /
  `weekly-review`, e.g. "plan my week," "add task: X," "sweep for tasks")
  continues to work exactly as before — the new agent absorbs these as
  on-demand modes alongside its autonomous cadence below. Quick single-item
  capture ("add a todo," "remind me to X tonight") bypasses the full ranking
  pass, per the reference repo's pattern.

## Autonomous cadence

No cron infrastructure exists in this workforce yet (confirmed via `CronList`
— zero scheduled jobs); this is new build.

- **Morning (scheduled)**: full ranking pass across everything in scope →
  writes today's picks directly onto today's section of the current weekly
  page → push notification with a one-line summary, inviting feedback in
  chat. Any reply from Nick is parsed as edits and applied back to the page —
  not a full re-plan, just the specific change requested.
- **Sunday morning specifically**: same as above, plus a forced top-3
  "week ahead" priorities framing included in the notification — this
  preserves `weekly-review`'s old forcing function as a special Sunday
  behavior of the new agent, rather than resurrecting it as a separate
  ritual/agent.
- **Daytime (event-driven)**: re-evaluates when underlying state changes (a
  new near-deadline item lands, a calendar shift happens) and only notifies
  if something crosses an urgency threshold worth interrupting Nick for — not
  on a fixed timer.
- **Evening (scheduled)**: reconciliation pass. Updates Tasks Tracker status
  and today's page based on what got done (see Completion detection below),
  and rolls unfinished items forward.

## Ranking ("what's worth working on next")

Composite score, not a single sort key:
- Deadline proximity
- Priority tier — read directly off the Tasks Tracker `Priority` field. No
  separate Projects Registry database for v1 — that's more structure than
  currently needed; can be added later if per-project defaults (goal, repo
  path, standing priority) become worth tracking centrally.
- Staleness — how long an item has sat untouched, so things don't silently
  rot in the Backlog
- That day's calendar bandwidth — a slammed meeting day suppresses proposing
  heavy deep-work blocks

## Completion detection (evening reconciliation)

Hybrid:
- **Passive inference** wherever a clean signal exists: checkbox state on the
  weekly page, git commits/PRs referencing a task, calendar attendance for
  meeting-shaped items.
- **Active ask** only for the leftover items with no signal either way (e.g.
  "no signal on 'read arXiv paper' — did that happen?") — minimizes how often
  Nick has to respond, while still catching gaps passive inference would miss.

## Scope and approval model

- **In scope for everything, including job-prep**: no personal/work wall for
  now, since Nick hasn't started at Link Ventures yet and all current "work"
  items are prep, tracked the same as personal/side projects. Revisit this
  boundary once he's actually working from a separate work computer with real
  employer material.
- **Checklist writes are always automatic, no approval gate.** Writing or
  editing a line on the weekly page has no real-world side effect — it's as
  reversible as Nick editing it himself. This is deliberately distinct from
  "acting."
- **Real execution is always explicitly gated, per item — but out of scope
  for v1.** Anything with an actual effect (spawning an agent to do project
  work, opening a PR, booking calendar time, sending anything external) would
  require Nick's explicit go-ahead, mirroring the reference repo's
  approval-gated HAL pattern. v1 of this system is the
  planning/prioritization/Notion-writing layer only — no autonomous
  code-spawning or other execution. The execution gate is designed into this
  spec as the seam for a later phase, not built now. This keeps the system
  compliant with the workforce-wide "propose, don't act" rule in
  `HQ/CLAUDE.md` for everything that actually does something, while removing
  the daily manual-curation burden for everything that doesn't.

## Explicitly out of scope for v1

- Any agent-spawning / autonomous execution of project work (future phase)
- A formal Projects Registry database (priority tiers read from Tasks Tracker
  directly instead)
- Calendar time-blocking / auto-creating calendar events (the `Calendar
  Synced` property is reserved for this but unused in v1)
- Any change to `standup-prep` or `canvas-sweep`
