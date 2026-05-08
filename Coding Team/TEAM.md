# Coding Team

> **Scope:** Code lifecycle support — writing, reviewing, and debugging.
> This team helps Nick move faster and ship cleaner code at work and on
> side projects.

---

## Team Purpose

Handle the three core stages of everyday coding work: writing new code,
reviewing it before committing, and diagnosing bugs when things break.
Each agent owns one stage cleanly — no overlap.

---

## Agents

| Agent | Folder | Primary job |
|---|---|---|
| Code Writer | `agents/code-writer/` | Implement features and functions directly into project files |
| Code Reviewer | `agents/code-reviewer/` | Review code for correctness, quality, security, and style |
| Debugger | `agents/debugger/` | Diagnose root causes and propose targeted fixes |

---

## Team Rules

| Rule | Detail |
|---|---|
| **Read HQ first** | Every agent reads `HQ/CLAUDE.md` before starting |
| **No emoji** | Never include emoji in any output |
| **Small scope** | Write or change only what was asked; no opportunistic refactors |
| **Tests required** | Code Writer must write tests for any non-trivial logic |
| **Propose fixes** | Debugger proposes; never applies fixes without confirmation |
| **Cite evidence** | Code Reviewer and Debugger outputs must reference `file:line` |
| **Save outputs** | Review reports and debug analyses go to `Coding Team/outputs/` |

---

## Output File Naming

```
YYYY-MM-DD_[agent]-[descriptor].md
```

Examples:
```
2026-05-07_review-auth-middleware.md
2026-05-08_debug-login-crash.md
2026-05-09_review-api-refactor.md
```

---

## Routing Guide

| Request type | Agent |
|---|---|
| "Write [function/feature]" | Code Writer |
| "Implement [X]" | Code Writer |
| "Add [X] to [file]" | Code Writer |
| "Review [file/diff/branch/function]" | Code Reviewer |
| "Check my code" | Code Reviewer |
| "Sanity check this" | Code Reviewer |
| "Debug [error/behavior]" | Debugger |
| "Why is [X] failing?" | Debugger |
| "Help me fix [bug]" | Debugger |
| "[Error message] — help" | Debugger |

---

*Team created: May 2026. Update when agents are added or responsibilities change.*
