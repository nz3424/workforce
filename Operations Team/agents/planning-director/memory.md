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
- 2026-07-20 — Add (batch, via "plan my week") — Nick deprioritized the Hermes integration cluster (12 Tasks Tracker rows) and the portfolio website: set Priority→Low and cleared the overdue Jul 14 due date on all 12 Hermes rows so they stop dominating daily ranking. Bumped "Continue quant learning track" to Priority High / Project Job Prep and folded in a transformer-architecture deep dive. Added 2 new Tasks Tracker rows (apartment move logistics — High priority, Job Prep-adjacent Personal; agent graphs / self-improving loops research — Medium, Research). Wrote real week-specific items onto Week of Jul 20 (2026-W30): swapped Monday's 3 Hermes Deep Work items for the quant/transformer deep dive; added IKEA (Tue Chores), workout (Tue Fitness), agent-graphs research (Wed Deep Work), apartment logistics kickoff (Wed Personal), long run (Wed Fitness), NYC-trip packing (Thu Personal), Amtrak 112 to NYC 9:11 AM (Fri Personal), Amtrak 149 home 5:04 PM (Sun Personal) — return-trip times pulled from the Amtrak eTicket/receipt emails (thread 19f673e00cdf2328). Added 3Blue1Brown backprop video to Backlog.
- 2026-07-21 — Auto-Morning — current week lookup found exactly one match (Week of Jul 20, 2026-W30), no rollover needed. Ranking pass surfaced "Continue quant learning track + transformer deep dive, get progress recap" [Job Prep] (score 130: High priority + 2 days overdue), "Write capstone README / postmortem" [Capstone] (score 115: Medium priority + 2wk+ overdue, due 2026-07-07 — Project/Area was null so tagged from task title since Notes didn't name one), and "Plan apartment move logistics" [Personal] (score 30: High priority, no due date). Calendar showed 0 hours booked 9am–6pm → top 3 selected. Wrote all 3 to Tuesday's Deep Work section. Note: Monday's "Continue quant learning..." item is still unchecked from yesterday's write — re-surfaced it for Tuesday per the ranking pass since it hasn't been marked Done, not treated as a same-day duplicate. Push notification not delivered (Remote Control inactive) but chat confirmation stands. Also noticed the stray null-title Tasks Tracker row flagged in yesterday's log is still present, untouched (Task name/Priority/Notes all null) — still likely leftover debug data, still flagged for Nick to delete. Could not verify Tasks Tracker item staleness (a `notion-query-data-sources` query for the `Created` column timed out) — ranking proceeded on due-date + priority only, which was already decisive for the top 3.
- 2026-07-21 — Add (direct edit, "update my weekly planner" re: IKEA moving to tomorrow) — Nick's IKEA trip moved from Tuesday to Wednesday. Moved the existing unchecked "Get furniture at IKEA" line on Week of Jul 20 (2026-W30) from Tuesday's Chores to Wednesday's Chores via a targeted `update_content` edit — no new item created, no Tasks Tracker row involved (single-day personal item already on the weekly page).
- 2026-07-21 — Add ("planning my day," 3 explicit Job Prep items for today) — Nick named the category directly (Job Prep, not Deep Work) despite these being deep-work-shaped tasks, so wrote as given rather than re-routing. Added to today's (Tuesday) Job Prep section on Week of Jul 20 (2026-W30): "Quant learning Track 2: activations + normalization", "Re-read QuantM business plan for deeper comprehension", "Review photonics + GPU weight storage + MATMUL principles from the past few days". No duplicates found against existing Tuesday Deep Work items (distinct from "Continue quant learning track + transformer deep dive" already there) or Tasks Tracker. Single-day items, so written directly to the weekly page — no Tasks Tracker rows created.

---

## Learned Preferences

<!-- Corrections or preferences Nick has expressed — category placement,
     ranking weights that felt off, notification tone, etc. -->
<!-- Format: Date — Observation -->

*(no entries yet)*

---

*Append entries below each section header. Date every entry.*
