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
| Summarizer | `agents/summarizer/` | Condenses articles, docs, papers, reports, long pasted text, and past Claude Code transcripts into structured summaries |
| Tech Radar | `agents/tech-radar/` | Tracks tools, libraries, and trends in Nick's areas of interest |
| Paper Writer | `agents/paper-writer/` | Writes LaTeX research papers on any topic; outputs `.tex` + `.bib` |

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

Research files saved to `Research Team/outputs/`:
```
YYYY-MM-DD_topic-name.md
```

Papers saved to `Research Team/papers/`:
```
YYYY-MM-DD_topic-name.tex
YYYY-MM-DD_topic-name.bib
```

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
| "Summarize this article / doc / paper / report" | Summarizer |
| "Give me the key points from [URL/text]" | Summarizer |
| "Recap what we've discussed about [topic] over the last N days" | Summarizer (topic-scoped, not the daily log — see below) |
| "What did I learn today?" / "Catch me up" | **Not Summarizer** — learning-log (`/recap`), see `Operations Team/agents/learning-log/agent.md` |
| "What's new in [area] this week/month?" | Tech Radar |
| "Should I look into [tool/library]?" | Tech Radar |
| "Write a paper on [topic]" | Paper Writer |
| "Give me a LaTeX paper on [topic]" | Paper Writer |

---

*Team created: May 2026. Update when agents are added or responsibilities change.*
