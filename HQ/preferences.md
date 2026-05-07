# preferences.md — Style & Formatting Defaults

> Agents: use this as the style guide for all outputs. When CLAUDE.md and this
> file conflict, CLAUDE.md wins.

---

## Output Formatting

| Context | Preferred format |
|---|---|
| Daily briefings | Bullet list, max 7 items, grouped by category |
| Research summaries | TL;DR (2–3 sentences) → Key Points → Sources |
| Code explanations | What it does → Why this approach → Any caveats |
| Email drafts | Subject line suggestion + body; flag tone assumptions |
| Weekly plans | Day-by-day table or grouped list, not dense prose |
| Task lists | Short imperative phrases ("Fix X", "Send Y") — no padding |

### General rules
- **Default length:** Short. If unsure, be shorter.
- **Headers:** Use them for anything over 3 sections; skip for short outputs
- **Bold:** Use sparingly — only for the most important term per section
- **Tables:** Great for comparisons and structured data; avoid for simple lists
- **Emoji:** None
- **Bullet depth:** Max 2 levels; if you need a 3rd level, restructure

---

## Email Formatting

- **Subject lines:** Specific and scannable — avoid vague subjects like
  "Following up" (prefer "Following up on SWE role — Nick Zhu")
- **Greeting:** "Hi [First name]," for most cases; "Dear [Name]," only for
  very formal contexts
- **Body:** 3–5 sentences for simple asks; short paragraphs; one clear ask
  per email
- **Closing:** "Best, Nick Zhu", One line, then sign-off on its own line
- **Attachments:** Always mention them explicitly in the body

### Email draft format (for drafts/ folder)
```
TO: [recipient]
SUBJECT: [suggested subject]
TONE NOTE: [brief note on tone assumptions made]

---

[email body]
```

---

## Code Style

> Update this section once you know your job's stack and conventions.

- **General:** Readable > clever; name things clearly; functions do one thing
- **Comments:** Explain *why*, not *what* — avoid restating what the code does
- **Error handling:** Always handle errors explicitly; no silent failures
- **File structure:** One concern per file where possible
- **Commit messages:** Imperative mood, present tense ("Add X", not "Added X")
- **PR descriptions:** What changed + why + how to test it

### Language-specific (fill in after starting job)
- **Primary language:** Javascript/Python
- **Linter / formatter:** ESlint (for JS), Ruff (for Python)
- **Test framework:** TBD
- **Repo conventions:** Follow typical conventions

---

## Research & Summaries

- **Default depth:** Surface-level brief first; offer to go deeper if desired
- **Sources:** Always cite; prefer primary sources over aggregators
- **Saved output format:** `YYYY-MM-DD_topic-name.md` in Research Team/outputs/
- **Confidence:** Flag uncertainty explicitly ("this may have changed since...")

---

## Calendar & Scheduling

- **Work hours:** Flexible; avoid scheduling before 8am or after 7pm unless
  necessary. For non-work days, avoid scheduling before 9:30am.
- **Deep work blocks:** Prefer late morning/early afternoon; mark as "Focus" in calendar title
- **Meeting prep:** Flag any meeting that needs prep material 24h in advance
- **Buffer time:** Try to leave 10–15 min between back-to-back meetings
---

*Update this file as your preferences evolve — especially the code style
section once you know your job's stack.*
