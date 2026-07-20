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
- **weekly_task_planner_data_source_id:** 1acfd14c-36cd-41ce-b6aa-6bca7deb9392
- **weekly_task_planner_url:** https://app.notion.com/p/14c1b18911df4ac087b0ad4baae516b3

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

- 2026-07-20 — Auto-Morning — wrote 3 Deep Work items to Week of Jul 20 (2026-W30), Monday: "Ideate on a full-stack project to build and deploy" [UNCLEAR project — no Project/Area set], "Connect Google Calendar to Hermes" [Hermes], "Connect Gmail to Hermes" [Hermes]. Calendar bandwidth: only an all-day event today, treated as <2h booked → top 3 selected. Noted a stray "test task — delete me after verifying" row in Tasks Tracker (score too low to surface in Deep Work, but likely leftover debug data — flagged for Nick).
- 2026-07-20 — Auto-Evening — all 3 of this morning's Monday Deep Work items still unchecked at reconciliation time, none meeting-shaped (no calendar attendance to cross-check). Asked Nick for a done/not-done signal on all 3; no reply within this run, so left unchecked and carried per spec — will be re-scored by tomorrow's ranking pass. No Tasks Tracker status changes made.

---

## Learned Preferences

<!-- Corrections or preferences Nick has expressed — category placement,
     ranking weights that felt off, notification tone, etc. -->
<!-- Format: Date — Observation -->

*(no entries yet)*

---

*Append entries below each section header. Date every entry.*
