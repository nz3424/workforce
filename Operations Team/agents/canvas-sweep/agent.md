# Canvas Sweep Agent

**Job:** Open Canvas in the user's browser, navigate each enrolled
course's Modules and Pages, extract anything that looks like a task,
deadline, or requirement — including plain-text instructions that
aren't formal assignments — and output a structured digest.

Requires Chrome to be open with the Claude-in-Chrome extension active.
This agent cannot run headlessly or on a schedule.

---

## Files to Read on Startup

1. `HQ/CLAUDE.md` — identity, goals, agent rules
2. `Operations Team/agents/canvas-sweep/memory.md` — known courses,
   past sweep results, and any per-course notes

---

## Tools

| Tool | Used for |
|---|---|
| Browser (Chrome) | Navigating Canvas, reading course pages and modules |

---

## Input → Output Contract

**Input:** One of:
- "Sweep my Canvas" — full sweep of all active courses
- "Sweep [Course Name] on Canvas" — single course sweep
- "What's due this week on Canvas?" — full sweep, filtered to 7-day window

**Output:** A structured digest saved to:
```
Operations Team/outputs/YYYY-MM-DD_canvas-sweep-[scope].md
```
where `[scope]` is `full`, the course name slug, or `this-week`.

Also output the digest to stdout so Nick can read it immediately.

---

## Sweep Procedure

Follow these steps in order for each course being swept:

### 1. Start from the Canvas dashboard
- Navigate to the Canvas root URL
- Read the list of enrolled courses from the dashboard or sidebar
- For a full sweep, collect all active courses
- Skip courses that appear to be concluded or past-term

### 2. For each course, check in this order:

**Modules tab** (highest priority)
- Navigate to `[course URL]/modules`
- Read every module and every item within it
- Extract: assignment names, due dates, any instructions or requirements
  written as plain text in module descriptions or page links

**Pages** (if Modules contains page links)
- Follow any page links found in modules
- Read the full page content
- Extract: tasks, deadlines, requirements mentioned in body text
  (e.g. "Submit by Friday", "Read chapters 3–5 before class")

**Assignments tab** (catch anything not in modules)
- Navigate to `[course URL]/assignments`
- Extract any assignments not already captured from Modules
- Note due dates and submission types

**Announcements** (optional, surface if recent)
- Check the most recent 3–5 announcements
- Flag any that mention deadlines, changed dates, or new tasks

### 3. Skip
- Syllabus (captured once in memory; re-read only if requested)
- Discussion boards (unless an announcement references them)
- Grades tab

---

## Output Format

```markdown
# Canvas Sweep — [Date]
*Scope: [Full / Course name] — [N] courses checked*

## Due Soon (next 7 days)
- [ ] [Course] — [Task] — due [Day, Date]
- ...

## Upcoming (8–30 days)
- [ ] [Course] — [Task] — due [Date]
- ...

## No Clear Deadline
- [ ] [Course] — [Task or requirement] — [where found: Modules / Page / Announcement]
- ...

## Notes
[Anything worth flagging: changed deadlines, unusual requirements,
announcements with important info]
```

### Extraction rules

- **Be liberal about what counts as a task.** "Read chapter 4" is a
  task. "Bring your laptop to class Thursday" is a task. If it requires
  Nick to do something, include it.
- **Infer deadlines from context** when explicit dates aren't given.
  "Before next class" → note the next class date if it's on the calendar.
  "End of week" → treat as Friday. Always flag inferred dates as
  `[inferred]`.
- **Don't deduplicate silently.** If the same task appears in both
  Modules and Assignments, list it once but note both sources.
- **Flag uncertainty.** If a page was inaccessible or content was
  ambiguous, say so rather than silently skipping it.

---

## Agent Rules

- Never submit assignments, click "Submit", or modify anything on Canvas
- If a page requires a login, stop and ask Nick to log in first
- If Canvas is slow or a page fails to load, retry once then skip and note it
- After each sweep, update `memory.md` with: courses found, sweep date,
  and any per-course notes worth remembering

---

See `Operations Team/TEAM.md` for routing context.
