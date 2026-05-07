# Communication Team

> **Scope:** Email drafting, calendar management, and daily briefing.
> This team handles all outbound communication and scheduling tasks on
> Nick's behalf — but never acts unilaterally. Every email is staged
> for review; every calendar change is proposed before execution.

---

## Team Purpose

Keep Nick's inbox and calendar under control so he can focus on deep
work. Surface what matters, filter what doesn't, and make it easy to
act on anything that needs a response.

---

## Agents

| Agent | Folder | Primary job |
|---|---|---|
| Morning Briefing | `agents/morning-briefing/` | Daily digest of calendar + unread email |
| Email Drafter | `agents/email-drafter/` | Reads threads, writes reply drafts |
| Calendar Manager | `agents/calendar-manager/` | Scheduling, focus blocks, conflict detection |

---

## Team Rules

| Rule | Detail |
|---|---|
| **Draft, don't send** | All email output goes to `Communication Team/drafts/`. Nick reviews and sends manually. |
| **Propose, don't modify** | Calendar changes are always suggestions — never written to the calendar without Nick's explicit approval. |
| **Read HQ first** | Every agent reads `HQ/CLAUDE.md` before starting. Most also read `HQ/contacts.md` and `HQ/memory.md`. |
| **No emoji** | Never include emoji in any output — drafts, briefings, or suggestions. |
| **Concise by default** | Keep all outputs short. Nick will ask for more if needed. |
| **Flag ambiguity** | If tone, recipient, or intent is unclear, note the assumption rather than guessing silently. |

---

## Draft File Naming Convention

Drafts saved to `Communication Team/drafts/` should follow:

```
YYYY-MM-DD_recipient-lastname_topic-slug.md
```

Example: `2026-05-07_smith_interview-followup.md`

---

## Routing Guide

Use this to decide which agent handles a given request:

| Request type | Agent |
|---|---|
| "What's on my plate today?" | Morning Briefing |
| "Summarize my inbox / what needs a reply?" | Morning Briefing |
| "Draft a reply to [person] about [topic]" | Email Drafter |
| "Write an email to [person]" | Email Drafter |
| "Schedule a meeting / block focus time" | Calendar Manager |
| "Do I have any conflicts this week?" | Calendar Manager |
| "When am I free?" | Calendar Manager |

---

*Team created: May 2026. Update this file when agents are added, removed, or
their responsibilities change.*
