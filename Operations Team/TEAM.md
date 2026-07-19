# Operations Team

> **Scope:** Day-to-day logistics — Canvas tracking, task management,
> weekly planning, and standup prep. This team keeps Nick organized
> and prevents things from falling through the cracks.

---

## Team Purpose

Handle the recurring operational overhead that would otherwise steal
focus from deep work. Surface what needs attention, when, and in a
format Nick can act on in under 2 minutes.

---

## Agents

| Agent | Folder | Primary job |
|---|---|---|
| Canvas Sweep | `agents/canvas-sweep/` | Scrapes Canvas course pages and modules for tasks and deadlines |
| Planning Director | `agents/planning-director/` | Maintains the Notion weekly planner, ranks tasks across all projects, and runs the morning/evening planning cadence automatically |
| Standup Prep | `agents/standup-prep/` | Generates daily standup summary for the new job |
| Learning Log | `agents/learning-log/` | Running log of what Nick learned each day; captures, recaps, and resurfaces it |

---

## Team Rules

| Rule | Detail |
|---|---|
| **Read HQ first** | Every agent reads `HQ/CLAUDE.md` before starting |
| **No emoji** | Never include emoji in any output |
| **Concise** | Task lists and summaries only — no preamble, no padding |
| **Propose, don't act** | Never modify calendar or send messages without Nick's approval |
| **Confirm before writing** | Task Planner must show a preview before committing sweep results to Notion |
| **Save outputs** | Persistent outputs go to `Operations Team/outputs/` |
| **Exception: Learning Log** | Learning Log does not use `outputs/` or the per-day naming below — it maintains one running file, `agents/learning-log/log.md` |

---

## Output File Naming

```
YYYY-MM-DD_[agent-name]-[descriptor].md
```

Examples:
```
2026-05-07_canvas-sweep-full.md
2026-05-09_task-plan.md
2026-05-10_weekly-review.md
2026-05-08_standup.md
```

---

## Routing Guide

| Request type | Agent |
|---|---|
| "What do I have due on Canvas?" | Canvas Sweep |
| "Sweep my Canvas courses" | Canvas Sweep |
| "Add task: [description]" | Planning Director |
| "Add tasks: [list]" | Planning Director |
| "Sweep for tasks" / "Task sweep" | Planning Director |
| "Plan my week" / "What do I need to do?" | Planning Director |
| "What's my week look like / Sunday review" | Planning Director |
| "Help me plan this week" | Planning Director |
| "What do I say at standup?" | Standup Prep |
| "Generate my standup for today" | Standup Prep |
| "Log: [what I learned]" / `/recap log [...]` | Learning Log |
| "Daily recap" / "What did I learn today?" / `/recap today` | Learning Log |
| "What did I learn recently?" / "Catch me up" / `/recap` | Learning Log |

---

*Team created: May 2026. Update when agents are added or responsibilities change.*
