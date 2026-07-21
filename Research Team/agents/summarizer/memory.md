# summarizer — Agent Memory

> Persistent memory for the Summarizer agent.
> Read on startup (after HQ/CLAUDE.md). Append only — never overwrite.

---

## Learned Preferences

<!-- Format or depth corrections Nick has made. -->
<!-- Format: Date — Observation -->

- 2026-07-21 — Scope broadened from "articles/docs/papers only" to general
  text summarization: also covers reports, long pasted/assistant text, and
  Claude Code transcripts (single-day or multi-day topic-scoped recaps).
  Transcript pulls reuse Operations Team's `extract_transcripts.py`
  (read-only) rather than reimplementing parsing. Stays fully out of
  `learning-log`'s lane — never touches `log.md`; "what did I learn
  today"/"catch me up" still routes to learning-log, not here. New
  "Thematic Multi-Session Recap" output format added for transcript-recap
  requests (theme-organized, not chronological). See `agent.md` for full spec.

---

## Summary Log

<!-- One line per summary produced. -->
<!-- Format: Date — Source — Topic — File saved (or "stdout") -->

*(no entries yet)*

---

*Append entries below each section header. Date every entry.*
