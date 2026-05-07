# /research-paper — Research → Paper Pipeline

Run Researcher then Paper Writer back-to-back on a single topic.
Research stays in-context only — no intermediate file saved to outputs/.

**Usage:** `/research-paper [topic]` or `/research-paper [topic] — [length or style hint]`

---

## Step 1 — Research

Read `HQ/CLAUDE.md` and `HQ/memory.md` for context before starting.

Perform web research on the topic following Researcher agent rules:
- Primary sources first: official docs, papers, engineering blogs from
  the source org. Aggregators only when primary sources aren't available.
- Flag sources older than 18 months with `[may be outdated]`
- Flag uncertain or contested claims — don't present speculation as fact
- Collect 8–15 key findings (enough substance to write a full paper)
- For each source, record full citation details: author(s), title, URL,
  publication/date — not just a one-liner

Organize findings into these buckets before moving to Step 2:
- **Background** — prerequisite concepts
- **Core findings** — main argument and technical content
- **Tradeoffs / caveats** — known pitfalls, open questions
- **Connection to Nick** — how this relates to current goals or projects
  from `HQ/memory.md` (skip if no clear connection)

Do NOT save a research output file. Hold all findings in context.

---

## Step 2 — Write the Paper

Using the research collected in Step 1, produce a LaTeX paper following
the full Paper Writer agent spec (see `Research Team/agents/paper-writer/agent.md`):

- Use the standard LaTeX template from that spec
- Map research buckets to paper sections:
  - Background findings → `\section{Background}`
  - Core findings → core section(s)
  - Tradeoffs → `\section{Discussion}`
- Cite every non-trivial claim with `\cite{}` and a matching `.bib` entry
- Default to Standard length (6–10 pages) unless the request says otherwise
- Author: Nick Zhu

Save both files to `Research Team/papers/`:
```
YYYY-MM-DD_topic-name.tex
YYYY-MM-DD_topic-name.bib
```

After saving, print:
1. File paths
2. One-paragraph plain-English summary of the paper's argument so Nick
   can verify the direction before compiling
3. Update `Research Team/agents/paper-writer/memory.md` with a one-line
   log entry
