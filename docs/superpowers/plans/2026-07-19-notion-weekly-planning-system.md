# Notion Weekly Planning System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `task-planner` and `weekly-review` with one new agent,
`planning-director`, that maintains a durable per-week Notion checklist,
autonomously ranks and writes a daily plan without Nick asking, and
reconciles what got done each evening — while keeping any real-world
side effects entirely out of v1.

**Architecture:** A new "Weekly Task Planner" Notion database (one page per
week, written additively) sits alongside the existing "Nick's Tasks Tracker"
database (system of record for structured, multi-day work). One new agent,
`Operations Team/agents/planning-director/`, owns both databases and runs in
three ways: on-demand (chat-triggered), and two unattended `launchd` jobs
(morning digest, evening reconciliation) that invoke headless `claude -p`
the same way the existing `com.nickzhu.claude-recap` job already does.

**Tech Stack:** Notion MCP tools (`mcp__claude_ai_Notion__*`), Google
Calendar/Gmail/Drive MCP tools, macOS `launchd`, zsh, `PushNotification`.

**Background reading (not required, but useful context):**
`docs/superpowers/specs/2026-07-19-notion-weekly-planning-design.md` — the
approved design spec this plan implements.

## Global Constraints

- Repo-tracked file changes (agent.md, memory.md, TEAM.md, deprecation
  banners) get committed at the end of each task — small, focused commits,
  per this workforce's convention. Never `git push` without asking Nick
  first (existing multi-agent-hygiene rule).
- Files created **outside** the repo (`~/.claude/scripts/*`,
  `~/Library/LaunchAgents/*.plist`) are not part of this git repo and are
  never committed.
- Nick's Tasks Tracker database ID: `359490b4-d1bb-805f-80fc-f62567f5153f`.
  Its (single) data source ID: `359490b4-d1bb-8070-b7c1-000bc919645d`.
  Nick's Notion user ID: `1f9d872b-594c-8187-9710-000286f94d86`. These are
  already resolved (from `Operations Team/agents/task-planner/memory.md`) —
  do not re-run `notion-search`/`notion-get-users` to rediscover them.
- Categories on every weekly page, always in this order: `Deep Work`,
  `Job Prep`, `Personal`, `Fitness`, `Chores`.
- v1 excludes any tool that could execute real-world side effects beyond
  Notion/Calendar reads-and-writes and email reads (no Bash, no git, no
  code-editing tools) for `planning-director` — this is what makes
  `--permission-mode dontAsk` safe for the unattended jobs. Do not add
  broader tool access "for flexibility."
- Never fabricate task content. If a source is ambiguous, mark it
  `[UNCLEAR]` and let Nick decide — same rule `task-planner` already
  follows.

---

### Task 1: Audit and fix Nick's Tasks Tracker schema

**Files:** None in the repo — this is a live Notion schema change.

**Interfaces:**
- Produces: `Notes` (renamed from `Description`), `Project/Area` (select:
  `Job Prep`/`Coding`/`Research`/`Personal`), `Source` (select:
  `Manual`/`Email`/`Drive`/`Canvas`/`Calendar`), `Agent Tag` (select:
  `planning-director`/`canvas-sweep`/`user`), `Created` (created-time) —
  all subsequent tasks that write to Nick's Tasks Tracker rely on these
  exact property names.

- [ ] **Step 1: Fetch and confirm the live schema**

Call `mcp__claude_ai_Notion__notion-fetch` with
`id: "359490b4-d1bb-805f-80fc-f62567f5153f"`. Confirm the returned schema
still shows exactly: `Assignee` (person), `Description` (text), `Due date`
(date), `Effort level` (select), `Priority` (select), `Status` (status),
`Task name` (title), `Task type` (multi_select). If it has already changed
from this, stop and re-derive Step 3's DDL from the actual current schema
before continuing — don't blindly run the statements below against a
schema that no longer matches.

- [ ] **Step 2: Check for existing data in the properties being dropped**

Call `mcp__claude_ai_Notion__notion-query-data-sources`:

```json
{
  "data": {
    "data_source_urls": ["collection://359490b4-d1bb-8070-b7c1-000bc919645d"],
    "query": "SELECT url, \"Task name\", \"Task type\", \"Effort level\" FROM \"collection://359490b4-d1bb-8070-b7c1-000bc919645d\" WHERE \"Task type\" IS NOT NULL OR \"Effort level\" IS NOT NULL"
  }
}
```

If this returns **any rows**, STOP. Show the rows to Nick and ask whether to
migrate the value into `Notes` before dropping, drop it anyway, or keep the
property. Do not proceed to Step 3 for whichever property has data until
Nick responds. If the query returns zero rows, proceed directly.

- [ ] **Step 3: Apply the schema change**

Call `mcp__claude_ai_Notion__notion-update-data-source`:

```json
{
  "data_source_id": "359490b4-d1bb-8070-b7c1-000bc919645d",
  "statements": "RENAME COLUMN \"Description\" TO \"Notes\"; ADD COLUMN \"Project/Area\" SELECT('Job Prep':blue, 'Coding':green, 'Research':purple, 'Personal':gray); ADD COLUMN \"Source\" SELECT('Manual':default, 'Email':blue, 'Drive':green, 'Canvas':orange, 'Calendar':purple); ADD COLUMN \"Agent Tag\" SELECT('planning-director':blue, 'canvas-sweep':orange, 'user':gray); ADD COLUMN \"Created\" CREATED_TIME; DROP COLUMN \"Task type\"; DROP COLUMN \"Effort level\""
}
```

- [ ] **Step 4: Verify**

Re-fetch with `notion-fetch` (`id: "359490b4-d1bb-805f-80fc-f62567f5153f"`).
Confirm the schema now shows: `Assignee`, `Notes`, `Due date`, `Priority`,
`Status`, `Task name`, `Project/Area`, `Source`, `Agent Tag`, `Created` —
and no longer shows `Task type` or `Effort level`.

- [ ] **Step 5: No commit needed**

This task changes only live Notion state, nothing in the git repo. Skip
straight to Task 2.

---

### Task 2: Create the Weekly Task Planner database

**Files:** None in the repo.

**Interfaces:**
- Consumes: nothing from Task 1.
- Produces: a new Notion database titled "Weekly Task Planner" with a data
  source ID that Task 3 and `planning-director`'s agent.md (Task 5) both
  reference. Record this ID — it does not yet exist anywhere, unlike the
  Tasks Tracker ID above.

- [ ] **Step 1: Create the database**

Call `mcp__claude_ai_Notion__notion-create-database`:

```json
{
  "title": "Weekly Task Planner",
  "schema": "CREATE TABLE (\"Week\" TITLE, \"Due Date\" DATE, \"Calendar Synced\" CHECKBOX)"
}
```

Omit `parent` — this creates it as a private workspace-root page, matching
where Nick's Tasks Tracker already lives (confirmed via its memory.md:
"Parent page: workspace root").

- [ ] **Step 2: Verify and record the IDs**

The tool response includes the new database's page ID and a
`<data-source url="collection://...">` tag with its data source ID. Fetch
it back with `notion-fetch` to confirm the schema matches (`Week` title,
`Due Date` date, `Calendar Synced` checkbox — nothing else). Write both IDs
down — they're needed verbatim in Task 3 and Task 6.

- [ ] **Step 3: No commit needed**

Live Notion state only. Continue to Task 3.

---

### Task 3: Bootstrap the current week's page

**Files:** None in the repo.

**Interfaces:**
- Consumes: the Weekly Task Planner data source ID from Task 2.
- Produces: the first live weekly page, in the exact template format
  `planning-director` (Task 5) will additively write into. Use this task's
  output to sanity-check that the template renders as intended in Notion
  before agent.md locks in the format.

- [ ] **Step 1: Compute this week's Monday/Sunday and ISO week number**

Run:

```bash
python3 -c "
import datetime
today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
sunday = monday + datetime.timedelta(days=6)
iso_year, iso_week, _ = monday.isocalendar()
print('Monday:', monday.isoformat())
print('Sunday:', sunday.isoformat())
print('Title:', f'Week of {monday.strftime(\"%b %-d\")} ({iso_year}-W{iso_week:02d})')
"
```

Use the printed `Title`, `Monday`, and `Sunday` values in Step 2 below —
don't hardcode a date from this plan's writing date.

- [ ] **Step 2: Create the page**

Call `mcp__claude_ai_Notion__notion-create-pages` with the Weekly Task
Planner's data source ID as parent (`type: "data_source_id"`). Properties:
title = the computed `Title`, and the date range via
`"date:Due Date:start"` = computed `Monday`, `"date:Due Date:end"` =
computed `Sunday`, `"date:Due Date:is_datetime"` = `0`.

Content (Notion-flavored Markdown — replace `<TASKS_TRACKER_URL>` with
`https://www.notion.so/359490b4d1bb805f80fcf62567f5153f`):

```markdown
## Backlog
- [ ]

### Monday
- [ ] Deep Work
- [ ] Job Prep
- [ ] Personal
- [ ] Fitness
- [ ] Chores

### Tuesday
- [ ] Deep Work
- [ ] Job Prep
- [ ] Personal
- [ ] Fitness
- [ ] Chores

### Wednesday
- [ ] Deep Work
- [ ] Job Prep
- [ ] Personal
- [ ] Fitness
- [ ] Chores

### Thursday
- [ ] Deep Work
- [ ] Job Prep
- [ ] Personal
- [ ] Fitness
- [ ] Chores

### Friday
- [ ] Deep Work
- [ ] Job Prep
- [ ] Personal
- [ ] Fitness
- [ ] Chores

### Saturday
- [ ] Deep Work
- [ ] Job Prep
- [ ] Personal
- [ ] Fitness
- [ ] Chores

### Sunday
- [ ] Deep Work
- [ ] Job Prep
- [ ] Personal
- [ ] Fitness
- [ ] Chores

# Projects Planner
[Open Nick's Tasks Tracker →](<TASKS_TRACKER_URL>)
```

- [ ] **Step 3: Verify**

Fetch the created page with `notion-fetch` and confirm: title matches,
`Due Date` shows the correct Monday→Sunday range, and the content shows
all 7 day sections plus Backlog plus the Tasks Tracker link, rendered as
real checkbox/to-do blocks (not literal `- [ ]` text — if it rendered as
plain text instead of checkboxes, the Markdown checkbox syntax didn't
convert; fix by re-reading the `notion://docs/enhanced-markdown-spec` MCP
resource for the correct to-do block syntax and retrying).

- [ ] **Step 4: No commit needed**

Live Notion state only. Continue to Task 4.

---

### Task 4: Archive task-planner and weekly-review

**Files:**
- Modify: `Operations Team/agents/task-planner/agent.md`
- Modify: `Operations Team/agents/weekly-review/agent.md`
- Modify: `Operations Team/TEAM.md`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: nothing later tasks depend on programmatically — this is
  documentation/routing cleanup, safe to do in parallel with Tasks 1–3 if
  running multiple workers, but sequenced here for a single implementer.

- [ ] **Step 1: Add a deprecation banner to task-planner**

In `Operations Team/agents/task-planner/agent.md`, insert immediately after
the `# Task Planner Agent` title line:

```markdown

**DEPRECATED as of 2026-07-19.** Replaced by
`Operations Team/agents/planning-director/`, which owns Nick's Tasks
Tracker directly and adds autonomous daily ranking on top of this agent's
Add/Sweep/Plan modes. Retained for historical reference only — no new
delegation should occur here.
```

- [ ] **Step 2: Add a deprecation banner to weekly-review**

In `Operations Team/agents/weekly-review/agent.md`, insert immediately
after the `# Weekly Review Agent` title line:

```markdown

**DEPRECATED as of 2026-07-19.** Replaced by
`Operations Team/agents/planning-director/`, whose Sunday morning run
folds in a forced top-3 "week ahead" digest — the same forcing function
this agent used to provide. Retained for historical reference only — no
new delegation should occur here.
```

- [ ] **Step 3: Update Operations Team/TEAM.md**

In the **Agents** table, replace the `Task Planner` and `Weekly Review`
rows with a single new row, and add it in alphabetical-ish position
matching the existing list order:

```markdown
| Planning Director | `agents/planning-director/` | Maintains the Notion weekly planner, ranks tasks across all projects, and runs the morning/evening planning cadence automatically |
```

Leave `Canvas Sweep`, `Standup Prep`, and `Learning Log` rows unchanged.

In the **Routing Guide** table, replace every row that pointed at Task
Planner or Weekly Review:

```markdown
| "Add task: [description]" | Planning Director |
| "Add tasks: [list]" | Planning Director |
| "Sweep for tasks" / "Task sweep" | Planning Director |
| "Plan my week" / "What do I need to do?" | Planning Director |
| "What's my week look like / Sunday review" | Planning Director |
| "Help me plan this week" | Planning Director |
```

Leave the Canvas Sweep, Standup Prep, and Learning Log rows unchanged.

- [ ] **Step 4: Commit**

```bash
cd "/Users/nzhu/ClaudeProjects/Workforce"
git add "Operations Team/agents/task-planner/agent.md" "Operations Team/agents/weekly-review/agent.md" "Operations Team/TEAM.md"
git commit -m "$(cat <<'EOF'
Archive task-planner and weekly-review, route to planning-director

Both agents are superseded by the new planning-director agent (Notion
structure + autonomous cadence). Left in place with deprecation banners
for historical reference rather than deleted.
EOF
)"
```

---

### Task 5: Write planning-director/agent.md

**Files:**
- Create: `Operations Team/agents/planning-director/agent.md`

**Interfaces:**
- Consumes: Tasks Tracker data source ID (`359490b4-d1bb-8070-b7c1-000bc919645d`,
  post-Task-1 schema), Weekly Task Planner data source ID (from Task 2 —
  substitute the real value in place of `<WEEKLY_DS_ID>` below).
- Produces: the full behavioral spec later tasks (6–11) reference by mode
  name (`Add`, `Sweep`, `Auto-Morning`, `Auto-Evening`).

- [ ] **Step 1: Write the agent spec**

Create `Operations Team/agents/planning-director/agent.md` with this exact
content (replace `<WEEKLY_DS_ID>` with the real data source ID recorded in
Task 2):

```markdown
# Planning Director Agent

**Job:** Own Nick's Notion planning surface end to end — the Weekly Task
Planner (per-week checklist) and Nick's Tasks Tracker (structured
multi-day work). Takes direct requests ("plan my day," "add task: X"),
and also runs unattended twice a day (morning digest, evening
reconciliation) so Nick never has to remember to invoke it. Replaces
`task-planner` and `weekly-review`.

---

## Files to Read on Startup

1. `HQ/CLAUDE.md` — identity, goals, agent rules
2. `HQ/memory.md` — active projects and open threads
3. `HQ/preferences.md` — output format rules
4. `Operations Team/agents/planning-director/memory.md` — database IDs,
   known source patterns, run history

---

## Tools

| Tool | Used for |
|---|---|
| Notion MCP (`notion-fetch`, `notion-search`, `notion-query-data-sources`) | Read Weekly Task Planner + Tasks Tracker state |
| Notion MCP (`notion-create-pages`) | Bootstrap a new week's page; add Tasks Tracker rows |
| Notion MCP (`notion-update-page`) | Additive edits to the current week's page; update Tasks Tracker row status |
| Gmail MCP (`search_threads`, `get_thread`) | Sweep: scan recent email for actionable items |
| Google Drive MCP (`list_recent_files`, `read_file_content`, `search_files`) | Sweep: scan recent Drive files |
| Calendar MCP (`list_events`) | Ranking: calendar bandwidth; Evening: meeting attendance signal |
| `PushNotification` | Morning digest notification |

No Bash, git, or code-editing tools. This is deliberate — v1 never
executes real-world side effects, only reads/writes Notion, Calendar, and
Gmail/Drive. Do not add broader tools without updating the design spec
first.

---

## Notion IDs

- Weekly Task Planner data source: `<WEEKLY_DS_ID>`
- Nick's Tasks Tracker database: `359490b4-d1bb-805f-80fc-f62567f5153f`
- Nick's Tasks Tracker data source: `359490b4-d1bb-8070-b7c1-000bc919645d`
- Nick's Notion user ID: `1f9d872b-594c-8187-9710-000286f94d86`

---

## Categories

Every weekly page day uses exactly these five, in this order: `Deep Work`,
`Job Prep`, `Personal`, `Fitness`, `Chores`. `Deep Work` items get an
inline project tag in brackets — use the specific project name if the
source Tasks Tracker row's Notes make one clear (e.g. `[BitNet]`,
`[Workforce]`), otherwise fall back to its `Project/Area` value (e.g.
`[Job Prep]`, `[Coding]`, `[Research]`).

---

## Current-week lookup (run at the start of every mode)

1. Fetch the Weekly Task Planner data source
   (`notion-query-data-sources`, SQL mode:
   `SELECT url, "Week", "date:Due Date:start", "date:Due Date:end" FROM "collection://<WEEKLY_DS_ID>"`).
2. Compute today's local date.
3. Find the row whose `Due Date` range contains today.
   - Exactly one match → that's the current week's page URL. Proceed.
   - Zero matches → run **Rollover** (below), then proceed with the newly
     created page.
   - Two or more matches → stop and ask Nick to resolve the overlap
     manually; do not guess.

## Rollover (only when no row covers today)

1. Find the most recent existing week (highest `Due Date` end before
   today).
2. Compute the new week's Monday/Sunday the same way Task 3 did:
   `monday = today - timedelta(days=today.weekday())`, `sunday = monday + timedelta(days=6)`,
   title `f"Week of {monday:%b %-d} ({iso_year}-W{iso_week:02d})"`.
3. Fetch the prior week's page content. Extract its `## Backlog` section
   verbatim.
4. Create the new page (same template as Task 3, Step 2) with that
   Backlog content carried forward unchanged into the new page's Backlog
   section.
5. For any Backlog item that has now survived 3+ rollovers (track this by
   keeping an HTML comment count marker next to each carried item, e.g.
   `- [ ] Update LinkedIn <!-- carried:3 -->`; increment on each rollover;
   start at 1 the first time an item is carried), surface it in the next
   digest for an explicit keep/drop decision instead of carrying it
   silently again.
6. Do not touch the prior week's page otherwise — it stays as a closed,
   unmodified archive.

---

## Modes

### Add (direct invocation: "add task: X", "add a todo", "remind me to X")

1. Decide destination:
   - Multi-day / structured / has its own deadline worth tracking over
     time → Tasks Tracker row. Set `Task name`, `Priority` (default
     Medium), `Due date` (if mentioned), `Project/Area` (infer from
     context; leave unset and flag if unclear), `Source: Manual`,
     `Agent Tag: user`, `Assignee: 1f9d872b-594c-8187-9710-000286f94d86`,
     `Notes` (≤20-word summary if extra context was given).
   - Single-day / personal one-off → append directly to the relevant
     category section of **today's** row on the current week's page (or
     `## Backlog` if no specific day applies), via `notion-update-page`
     `update_content` with a narrow `old_str` anchor (the smallest block
     containing both the `### <Weekday>` header and the target category
     line — never a bare category line alone, which can match multiple
     days).
2. Run a light duplicate check: `notion-query-data-sources` against
   whichever destination, matching on significant word overlap in the
   title. If a close match exists and isn't `Done`, surface it and ask
   whether to add anyway, update the existing item, or cancel.
3. Confirm to Nick in one line: where it went and what got set.

### Sweep (direct invocation: "sweep for tasks", "task sweep")

Identical sourcing and preview-then-confirm behavior to the old
`task-planner`'s Sweep mode (email last 48h, Drive last 48h, Canvas-sweep
outputs last 7d, Calendar next 7d) — candidates always go to **Tasks
Tracker** (never directly onto the weekly page), tagged `Source` per
origin and `Agent Tag: planning-director`. Show the full preview and wait
for Nick's "yes/edit/cancel" before writing anything. Do not skip the
confirmation step even though writes elsewhere in this agent are
automatic — Sweep pulls from ambiguous external sources and needs human
judgment on relevance, unlike the ranking pass below which only reorders
things Nick already put in the system.

### Ranking ("what's worth working on next" — used by on-demand Plan and both Auto modes)

For every open Tasks Tracker row (`Status` ≠ `Done`) and every unchecked
Backlog item on the current week's page, compute a score:

- `+100` if due today or overdue
- `+50` if due within 3 days
- `+20` if due within 7 days
- `+30` / `+15` / `+5` for `Priority` High / Medium / Low
- `+10` per week the item has sat with no status change or edit, past an
  initial 2-week grace period, capped at `+40` (staleness)
- Backlog items with no `Priority` default to the Medium tier (`+15`) for
  scoring purposes only — don't write a Priority value onto a Backlog line

Fetch the current day's Calendar events (`list_events`) to gauge
bandwidth: count hours already booked between 9am–6pm today.
- `< 2 hours booked` → select the top 3 scored items for today's `Deep
  Work` section
- `2–4 hours booked` → top 2
- `> 4 hours booked` → top 1

Selected Tasks Tracker items become `Deep Work` lines on today's section,
formatted `- [ ] <imperative restatement of Task name> [<project tag>]`.
Don't duplicate an item that's already sitting unchecked in today's
`Deep Work` section from a prior write.

### On-demand Plan (direct invocation: "plan my day," "plan my week," "what do I need to do")

1. Run current-week lookup.
2. Run Ranking (above).
3. Write the selected items into today's `Deep Work` section via
   `update_content` (same anchoring rule as Add mode).
4. Reply in chat with what was written — don't wait for approval, this is
   the same "checklist writes are automatic" rule the Auto modes use, just
   triggered manually instead of on a timer.
5. If Nick replies with a change ("swap X for Y," "drop the gym item"),
   apply it as a targeted edit to the page — never a full re-plan unless
   he asks for one.

### Auto-Morning (fired only by the scheduled launchd job, never manually)

1. Run current-week lookup (this also handles Monday rollover).
2. Run Ranking and write today's `Deep Work` section, same as On-demand
   Plan.
3. **If today is Sunday:** also compute a forced top-3 "week ahead" list —
   take the 3 highest-scored items across the *entire upcoming week's*
   open Tasks Tracker rows (not just today), and include them in the
   notification as a distinct "This Week's Top 3" line, forcing a ranked
   choice the same way the old `weekly-review` did. Do not write the
   top-3 onto the page itself — it's a notification-only framing, the page
   only ever gets today's `Deep Work` section.
4. Send exactly one `PushNotification`: message format
   `"Today's plan is up — N items across [categories with items]. Top: [highest-scored item name]."`
   (on Sundays, append `" Week's top 3: [item], [item], [item]."` — keep
   the whole message under 200 characters; drop to just the count and top
   item if the week's-top-3 addition would exceed it).
5. If Nick replies to the notification/session with feedback, apply it as
   a targeted page edit — same rule as On-demand Plan step 5.

### Auto-Evening (fired only by the scheduled launchd job, never manually)

**Scope note vs. the design spec:** the spec listed git commits/PRs as a
possible passive-completion signal alongside checkboxes and calendar
attendance. This agent deliberately has no Bash/git tool access (see the
Tools table above) — that's what makes `--permission-mode dontAsk` safe
for the unattended run. Passive inference here is therefore checkbox state
and calendar attendance only; git-based inference is out of scope for v1,
consistent with "no execution tools" rather than an oversight.

1. Run current-week lookup.
2. **Passive inference** — for every item written to today's page this
   morning (or already present): checked (`- [x]`) → mark done. For any
   corresponding Tasks Tracker row, set `Status: Done`. Cross-check
   calendar-shaped items (anything that names a meeting/call) against
   `list_events` attendance — if the event existed on today's calendar,
   treat it as done even if the box wasn't checked.
3. **Leftover items** — anything still unchecked with no passive signal:
   collect them into a short list.
4. **If the leftover list is non-empty**, ask Nick directly (this is the
   one interactive moment in the unattended evening run — if nobody
   responds because it's truly unattended, leave those items as unchecked
   and carried, don't block): "No signal on: [item], [item] — done or
   not?" Apply whatever response comes back; if none comes back in this
   run, leave them unchecked (they'll be picked up again by tomorrow's
   ranking pass, which reads current Notion state fresh each time).
5. Items still unchecked at the end of this mode remain on today's
   section as-is (the additive model means nothing gets deleted) — tomorrow
   morning's Ranking pass will naturally re-score and may re-select them.
6. No notification is sent for a normal Auto-Evening run — this is a
   quiet reconciliation pass, consistent with how `learning-log`'s
   unattended `/recap auto` also stays quiet (output only reaches a log
   file, not Nick directly).

---

## Agent Rules

- Checklist writes (Add's single-day path, Ranking's Deep Work writes,
  Auto-Evening's checkbox/status updates) never require approval — they
  have no real-world side effect.
- Tasks Tracker Sweep-sourced writes always require Nick's explicit
  confirmation of the preview first — never silently write swept
  candidates.
- Never invent a task. If a source is ambiguous, mark it `[UNCLEAR]` in
  whatever preview or leftover list it appears in, and let Nick decide.
- Never modify a past week's page. Only the current week's page is ever
  written to.
- Never add tools beyond the table above without updating the design spec
  first — the "no execution" boundary in v1 depends on this agent
  literally having no way to do anything but read/write Notion, Calendar,
  and Gmail/Drive.
- Append a one-line entry to `memory.md` after every Add, Sweep,
  Auto-Morning, and Auto-Evening run (see memory.md's own format).

---

See `Operations Team/TEAM.md` for routing context.
```

- [ ] **Step 2: Commit**

```bash
cd "/Users/nzhu/ClaudeProjects/Workforce"
git add "Operations Team/agents/planning-director/agent.md"
git commit -m "$(cat <<'EOF'
Add planning-director agent spec

Owns the Weekly Task Planner + Nick's Tasks Tracker, with on-demand
modes plus two unattended cadences (morning ranking/digest, evening
reconciliation). No execution tools in v1 — Notion/Calendar/Gmail/Drive
only.
EOF
)"
```

---

### Task 6: Write planning-director/memory.md

**Files:**
- Create: `Operations Team/agents/planning-director/memory.md`

**Interfaces:**
- Consumes: Weekly Task Planner data source ID (Task 2), Tasks Tracker IDs
  (already known, see Global Constraints).
- Produces: the memory file `agent.md`'s "Files to Read on Startup"
  section (Task 5) already points to.

- [ ] **Step 1: Write the memory file**

Create `Operations Team/agents/planning-director/memory.md` (replace
`<WEEKLY_DS_ID>` and `<WEEKLY_DB_PAGE_URL>` with the real values from Task 2):

```markdown
# planning-director — Agent Memory

> Persistent memory for the Planning Director agent.
> Read on startup. Append only — never overwrite.

---

## Notion IDs

<!-- Carried over from task-planner/memory.md and weekly-review's setup;
     do not re-run bootstrap discovery for these. -->

- **tasks_tracker_database_id:** 359490b4-d1bb-805f-80fc-f62567f5153f
- **tasks_tracker_data_source_id:** 359490b4-d1bb-8070-b7c1-000bc919645d
- **notion_user_id:** 1f9d872b-594c-8187-9710-000286f94d86
- **weekly_task_planner_data_source_id:** <WEEKLY_DS_ID>
- **weekly_task_planner_url:** <WEEKLY_DB_PAGE_URL>

---

## Predecessor Notes

<!-- Inherited context from the deprecated task-planner and weekly-review
     agents. Historical only. -->

- 2026-05-07 — task-planner bootstrap found existing "Nick's Tasks
  Tracker" database; ran one sweep (3 tasks added) before deprecation.
- 2026-07-19 — Tasks Tracker schema corrected: `Description` → `Notes`,
  added `Project/Area`/`Source`/`Agent Tag`/`Created`, dropped `Task
  type`/`Effort level` (see Task 1 of the implementation plan).

---

## Known Source Patterns

<!-- Patterns learned from sweeps — helps deduplication and extraction. -->
<!-- Format: Date — Source — Pattern observed -->

*(no entries yet)*

---

## Run Log

<!-- One line per Add / Sweep / Auto-Morning / Auto-Evening run. -->
<!-- Format: Date Time — Mode — outcome -->

*(no entries yet)*

---

## Learned Preferences

<!-- Corrections or preferences Nick has expressed — category placement,
     ranking weights that felt off, notification tone, etc. -->
<!-- Format: Date — Observation -->

*(no entries yet)*

---

*Append entries below each section header. Date every entry.*
```

- [ ] **Step 2: Commit**

```bash
cd "/Users/nzhu/ClaudeProjects/Workforce"
git add "Operations Team/agents/planning-director/memory.md"
git commit -m "Add planning-director memory file with carried-over Notion IDs"
```

---

### Task 7: Create the /plan global command

**Files:**
- Create: `~/.claude/commands/plan.md` (outside the repo, mirrors
  `~/.claude/commands/recap.md`'s pattern — global entry point, not
  project-specific)

**Interfaces:**
- Consumes: `Operations Team/agents/planning-director/agent.md` (Task 5) —
  this command only routes to it.
- Produces: the exact invocation string the Task 9/10 launchd scripts call
  (`claude -p "/plan auto-morning"` and `claude -p "/plan auto-evening"`).

- [ ] **Step 1: Write the command file**

Create `~/.claude/commands/plan.md`:

```markdown
# /plan — Planning Director

Global entry point for the Planning Director agent
(`Operations Team/agents/planning-director/` in the Workforce project).
Works from any directory — this file is the only place an absolute path
lives; if the Workforce project ever moves, update the path here and
nothing else breaks.

**Usage:**
- `/plan` or `/plan day` — on-demand Plan mode: "plan my day"
- `/plan week` — on-demand Plan mode, weekly framing: "plan my week"
- `/plan add [description]` — Add mode
- `/plan sweep` — Sweep mode
- `/plan auto-morning` — unattended morning digest, fired only by the
  scheduled `com.nickzhu.planning-director-morning` launchd job. Not
  intended for manual use.
- `/plan auto-evening` — unattended evening reconciliation, fired only by
  the scheduled `com.nickzhu.planning-director-evening` launchd job. Not
  intended for manual use.

---

## Step 1 — Load the agent spec

Read
`/Users/nzhu/ClaudeProjects/Workforce/Operations Team/agents/planning-director/agent.md`
in full. It defines every mode. Follow it exactly — this command file only
routes to it and parses arguments.

Also read
`/Users/nzhu/ClaudeProjects/Workforce/Operations Team/agents/planning-director/memory.md`.

## Step 2 — Parse arguments and dispatch

- No arguments, or `day` → **On-demand Plan** (daily framing).
- `week` → **On-demand Plan**, but frame the reply around the week ahead
  (still only ever writes today's `Deep Work` section — the weekly framing
  is about what Nick sees in chat, not an extra page write).
- `add [description]` → **Add mode**, everything after `add` is the task
  description.
- `sweep` → **Sweep mode**.
- `auto-morning` → **Auto-Morning mode**. Follow the agent spec's
  Auto-Morning contract exactly, including the Sunday special case.
- `auto-evening` → **Auto-Evening mode**.

## Step 3 — Confirm

Short confirmation only, following whatever output format the invoked
mode's section of `agent.md` specifies.
```

- [ ] **Step 2: Verify it's picked up**

Run `claude -p "/plan add test task — delete me after verifying" --permission-mode dontAsk` from the Workforce directory in a scratch check, confirm it
creates a row in Nick's Tasks Tracker, then delete that test row manually
in Notion (via `notion-update-page` with `in_trash`-style removal isn't
exposed on pages directly — instead ask Nick to trash it from the Notion
UI, or use `notion-fetch` to locate it and leave a note in the task
summary reminding him to delete the test row).

- [ ] **Step 3: No commit needed**

`~/.claude/commands/` is outside the git repo. Continue to Task 8.

---

### Task 8: Create the morning automation

**Files:**
- Create: `~/.claude/scripts/run-planning-director-morning.sh` (outside
  the repo)
- Create: `~/Library/LaunchAgents/com.nickzhu.planning-director-morning.plist`
  (outside the repo)

**Interfaces:**
- Consumes: `/plan auto-morning` (Task 7).
- Produces: nothing later tasks depend on — this is the terminal delivery
  mechanism for the morning cadence.

- [ ] **Step 1: Write the script**

Create `~/.claude/scripts/run-planning-director-morning.sh`:

```bash
#!/bin/zsh
# Invoked each morning by
# ~/Library/LaunchAgents/com.nickzhu.planning-director-morning.plist.
# launchd's environment has no shell profile sourced, so PATH is hardcoded.

CLAUDE_BIN="/Users/nzhu/.nvm/versions/node/v26.1.0/bin/claude"
WORKFORCE_DIR="/Users/nzhu/ClaudeProjects/Workforce"

cd "$WORKFORCE_DIR" || exit 1

exec "$CLAUDE_BIN" -p "/plan auto-morning" --permission-mode dontAsk
```

Make it executable: `chmod +x ~/.claude/scripts/run-planning-director-morning.sh`

- [ ] **Step 2: Write the launchd plist**

Create `~/Library/LaunchAgents/com.nickzhu.planning-director-morning.plist`
(picking `07:03` rather than the round `07:00`, matching this workforce's
existing off-the-hour convention seen in the recap job):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nickzhu.planning-director-morning</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/zsh</string>
        <string>-lc</string>
        <string>/Users/nzhu/.claude/scripts/run-planning-director-morning.sh</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>3</integer>
    </dict>

    <key>RunAtLoad</key>
    <false/>

    <key>StandardOutPath</key>
    <string>/Users/nzhu/.claude/logs/planning-director-morning-cron.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/nzhu/.claude/logs/planning-director-morning-cron.log</string>
</dict>
</plist>
```

- [ ] **Step 3: Load it**

```bash
launchctl load ~/Library/LaunchAgents/com.nickzhu.planning-director-morning.plist
launchctl list | grep planning-director-morning
```

Expected: the second command prints a line containing
`com.nickzhu.planning-director-morning`.

- [ ] **Step 4: Manually trigger once to verify end-to-end**

```bash
launchctl start com.nickzhu.planning-director-morning
sleep 30
cat /Users/nzhu/.claude/logs/planning-director-morning-cron.log
```

Confirm the log shows a completed run (no error, mentions writing to
today's Deep Work section). Then check: did a `PushNotification` actually
arrive (desktop notification, or phone if Remote Control is connected)?
**This was flagged as unverified during design — confirm it here for
real.** If no notification arrives despite the log showing a successful
run, that confirms `PushNotification` doesn't fire from headless `claude
-p` sessions — note this finding in `planning-director/memory.md` under
Learned Preferences, and flag it to Nick so Task 10's morning-briefing
integration becomes the primary (not just backup) delivery channel.

- [ ] **Step 5: No commit needed**

Both files are outside the git repo. Continue to Task 9.

---

### Task 9: Create the evening automation

**Files:**
- Create: `~/.claude/scripts/run-planning-director-evening.sh` (outside
  the repo)
- Create: `~/Library/LaunchAgents/com.nickzhu.planning-director-evening.plist`
  (outside the repo)

**Interfaces:**
- Consumes: `/plan auto-evening` (Task 7).
- Produces: nothing later tasks depend on.

- [ ] **Step 1: Write the script**

Create `~/.claude/scripts/run-planning-director-evening.sh`:

```bash
#!/bin/zsh
# Invoked each evening by
# ~/Library/LaunchAgents/com.nickzhu.planning-director-evening.plist.
# launchd's environment has no shell profile sourced, so PATH is hardcoded.

CLAUDE_BIN="/Users/nzhu/.nvm/versions/node/v26.1.0/bin/claude"
WORKFORCE_DIR="/Users/nzhu/ClaudeProjects/Workforce"

cd "$WORKFORCE_DIR" || exit 1

exec "$CLAUDE_BIN" -p "/plan auto-evening" --permission-mode dontAsk
```

Make it executable: `chmod +x ~/.claude/scripts/run-planning-director-evening.sh`

- [ ] **Step 2: Write the launchd plist**

Create `~/Library/LaunchAgents/com.nickzhu.planning-director-evening.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nickzhu.planning-director-evening</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/zsh</string>
        <string>-lc</string>
        <string>/Users/nzhu/.claude/scripts/run-planning-director-evening.sh</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>21</integer>
        <key>Minute</key>
        <integer>7</integer>
    </dict>

    <key>RunAtLoad</key>
    <false/>

    <key>StandardOutPath</key>
    <string>/Users/nzhu/.claude/logs/planning-director-evening-cron.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/nzhu/.claude/logs/planning-director-evening-cron.log</string>
</dict>
</plist>
```

- [ ] **Step 3: Load and verify, same pattern as Task 8**

```bash
launchctl load ~/Library/LaunchAgents/com.nickzhu.planning-director-evening.plist
launchctl list | grep planning-director-evening
launchctl start com.nickzhu.planning-director-evening
sleep 30
cat /Users/nzhu/.claude/logs/planning-director-evening-cron.log
```

Confirm the log shows a completed run and, in Notion, that today's checked
boxes got their corresponding Tasks Tracker rows marked `Done`.

- [ ] **Step 4: No commit needed**

Both files are outside the git repo. Continue to Task 10.

---

### Task 10: Add "Today's Plan" section to morning-briefing

**Files:**
- Modify: `Communication Team/agents/morning-briefing/agent.md`

**Interfaces:**
- Consumes: the current week's Weekly Task Planner page (read-only) —
  same database Task 2/5 produced.
- Produces: nothing later tasks depend on.

This mirrors the existing, working integration where `morning-briefing`
already pulls a read-only "Yesterday, You Learned" section from
`learning-log/log.md` — same shape, new source.

- [ ] **Step 1: Add the read-only source to "Files to Read on Startup"**

In `Communication Team/agents/morning-briefing/agent.md`, in the numbered
"Files to Read on Startup" list, add after the existing `learning-log/log.md`
line:

```markdown
7. Nick's Weekly Task Planner (Notion, via `notion-fetch` on the current
   week's page — resolve "current week" the same way
   `planning-director/agent.md`'s "Current-week lookup" section does) —
   read-only, today's `Deep Work` and `Job Prep` sections only, for the
   "Today's Plan" callout
```

- [ ] **Step 2: Add the Notion tool to the Tools table**

Add a row to the `## Tools` table:

```markdown
| Notion MCP (`notion-fetch`, `notion-query-data-sources`) | Read-only: today's Deep Work / Job Prep items for "Today's Plan" |
```

- [ ] **Step 3: Add the section to the Output Format template**

In the `## Output Format` code block, insert a new section after
`## Open Threads` and before `## Yesterday, You Learned`:

```markdown
## Today's Plan
- [Item from today's Deep Work section]
- [Item from today's Job Prep section]
- ...
```

And add a corresponding rule under "### Rules for each section":

```markdown
**Today's Plan**
- Pull only today's `Deep Work` and `Job Prep` checklist items from the
  current week's Weekly Task Planner page — never other categories, never
  other days
- Read-only — never write to the Weekly Task Planner from this agent
- Skip this section entirely if today's Deep Work and Job Prep sections
  are both empty
- Cap at 5 bullets combined; if more, list the highest-priority items and
  note "+N more on the Weekly Task Planner"
```

- [ ] **Step 4: Note the backup-channel role in Agent Rules**

Add to the `## Agent Rules` list:

```markdown
- "Today's Plan" is a read-only mirror of `planning-director`'s morning
  write — if `planning-director`'s `PushNotification` isn't reaching
  Nick reliably from its unattended run (see its memory.md), this section
  is the guaranteed-delivery fallback, since this agent already emails
  Nick directly every morning.
```

- [ ] **Step 5: Commit**

```bash
cd "/Users/nzhu/ClaudeProjects/Workforce"
git add "Communication Team/agents/morning-briefing/agent.md"
git commit -m "$(cat <<'EOF'
Add read-only Today's Plan section to morning-briefing

Mirrors the existing Yesterday-You-Learned integration pattern. Gives
planning-director's morning digest a guaranteed-delivery channel via
email, independent of whether PushNotification reaches Nick from a
headless run.
EOF
)"
```

---

### Task 11: End-to-end verification pass

**Files:** None — verification only.

**Interfaces:**
- Consumes: everything from Tasks 1–10.

- [ ] **Step 1: Confirm both launchd jobs are loaded**

```bash
launchctl list | grep planning-director
```

Expected: two lines, `com.nickzhu.planning-director-morning` and
`com.nickzhu.planning-director-evening`, both with exit status `0` from
their manual test runs in Tasks 8/9.

- [ ] **Step 2: Confirm the deprecated agents route correctly**

Ask (in a normal interactive session): "Plan my week." Confirm the
response comes from `planning-director`, not `task-planner` or
`weekly-review` — check `Operations Team/TEAM.md`'s routing table matches
what actually got invoked.

- [ ] **Step 3: Confirm the Notion structure is coherent**

Fetch the current week's Weekly Task Planner page and Nick's Tasks
Tracker. Confirm: today's `Deep Work` section has real items (not the
empty template), any items sourced from Tasks Tracker rows are tagged
`[project]` correctly, and the bottom-of-page link to Tasks Tracker
resolves.

- [ ] **Step 4: Report to Nick**

Summarize: what's live (both databases, the new agent, both launchd
jobs), what got archived (`task-planner`, `weekly-review` — deprecated in
place, not deleted), whether `PushNotification` was confirmed working or
whether morning-briefing's "Today's Plan" is the primary channel instead,
and remind him that `git push` hasn't happened automatically — ask if he
wants the accumulated commits from Tasks 4–6 and 10 pushed now.

- [ ] **Step 5: No commit needed** — this task only verifies prior work.
