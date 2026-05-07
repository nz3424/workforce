# Research Team

> **Scope:** On-demand research, content summarization, and ongoing
> technology tracking. This team produces structured, citable outputs
> that Nick can act on or build from — not walls of text.

---

## Team Purpose

Help Nick build deep technical knowledge and stay current without
spending hours reading. Produce briefs he can scan in under 2 minutes,
with sources he can follow up on if he wants more depth.

---

## Agents

| Agent | Folder | Primary job |
|---|---|---|
| Researcher | `agents/researcher/` | Deep-dive research reports on any topic |
| Summarizer | `agents/summarizer/` | Condenses articles, docs, and papers into structured summaries |
| Tech Radar | `agents/tech-radar/` | Tracks tools, libraries, and trends in Nick's areas of interest |

---

## Team Rules

| Rule | Detail |
|---|---|
| **Read HQ first** | Every agent reads `HQ/CLAUDE.md` before starting |
| **Cite sources** | Always include sources; prefer primary over aggregators |
| **Flag uncertainty** | Note when information may be outdated or confidence is low |
| **Short by default** | Lead with TL;DR; offer to go deeper rather than front-loading everything |
| **Save outputs** | All research outputs go to `Research Team/outputs/` |
| **No emoji** | Never include emoji in any output |

---

## Output File Naming

All files saved to `Research Team/outputs/` follow:

```
YYYY-MM-DD_topic-name.md
```

Example: `2026-05-07_react-server-components.md`

---

## Output Format (default)

From `HQ/preferences.md`:

```
## TL;DR
[2–3 sentences: what this is, why it matters to Nick]

## Key Points
- ...

## Sources
- [Title](url) — one-line description
```

---

## Routing Guide

| Request type | Agent |
|---|---|
| "Research [topic] for me" | Researcher |
| "What is [technology/concept]?" | Researcher |
| "Summarize this article / doc / paper" | Summarizer |
| "Give me the key points from [URL/text]" | Summarizer |
| "What's new in [area] this week/month?" | Tech Radar |
| "Should I look into [tool/library]?" | Tech Radar |

---

*Team created: May 2026. Update when agents are added or responsibilities change.*
