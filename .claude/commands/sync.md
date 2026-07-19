# /sync — Workforce Git Sync

Sync the Workforce repo to GitHub. Follow these steps exactly:

## Step 0 — Pin to repo root
Before running any git command, resolve the actual repo root:
```
REPO=$(git -C /Users/nzhu/ClaudeProjects/Workforce rev-parse --show-toplevel)
```
Run ALL subsequent git commands as `git -C "$REPO" <command>` to ensure
you're always operating on the real working directory, not a worktree
or sandbox default.

## Step 1 — Fetch remote
```
git -C "$REPO" fetch origin
```

## Step 2 — Compare working directory vs. GitHub
```
git -C "$REPO" diff origin/main --stat
git -C "$REPO" diff origin/main --name-status
git -C "$REPO" log HEAD..origin/main --oneline
```

Report in this format:
```
Local vs. GitHub (origin/main)
  Files changed: <N, or "none — working directory matches GitHub">

  Modified:        <file>  ...
  Added locally:   <file>  ...
  Deleted locally: <file>  ...
  Remote-only commits: <hash message> ...  (or "none")
```

If working directory matches GitHub exactly: report "Already in sync." and stop.

## Step 3 — Handle remote-only changes
Check `git -C "$REPO" log HEAD..origin/main --oneline`:

- **Remote has commits, no local changes:** Run `git -C "$REPO" pull origin main`.
  Report "Pulled N commits. Up to date." and stop.
- **Remote has commits AND local changes exist:** Stop and warn:
  "GitHub has commits your local directory doesn't. Pull and merge before syncing."
  List the remote commits. Do not commit or push.
- **Local is ahead or even:** Continue to Step 4.

## Step 4 — Stage changes and generate commit message
```
git -C "$REPO" add -A
```

Categorize staged changes into:
- **Structural** — agent specs, TEAM.md, CLAUDE.md, HQ files, .gitignore,
  .claude/commands/, new agents
- **Memory** — any file named `memory.md` or in `outputs/` or `drafts/`

Build the commit message:
- **Only memory files:** `Update agent memory — [YYYY-MM-DD]`
- **Only structural:** Describe what changed specifically
- **Mixed:**
  ```
  <Short description of structural change>

  Also update agent memory files
  ```
- **Multiple structural changes:**
  ```
  Update [summary]

  - Change one
  - Change two
  ```

Subject line: under 60 characters, imperative mood ("Add", "Update", "Fix").

## Step 5 — Confirmation gate

**If changes are structural (or mixed):**
Stop and show a confirmation prompt before doing anything irreversible:

```
Ready to commit and push:

  Commit message: "<generated message>"
  Files:
    <list of staged files>
  Destination: origin/main

Proceed? (yes / edit / cancel)
```

Wait for Nick's response:
- **"yes"** — continue to Step 6
- **"edit"** — ask what to change (message, files to exclude, etc.),
  update accordingly, re-show the prompt, wait again
- **"cancel"** — run `git -C "$REPO" reset HEAD` to unstage everything
  and report "Cancelled — no changes pushed."

**If changes are memory-only:**
Skip the confirmation prompt and proceed directly to Step 6.
(Memory commits are low-stakes and frequent — no need to interrupt.)

## Step 6 — Commit
```
git -C "$REPO" commit -m "<generated message>"
```
Skip if no new local changes were staged (only unpushed commits existed).

## Step 7 — Push
```
git -C "$REPO" push origin main
```

## Step 8 — Report
```
Synced to GitHub.
Committed: <commit subject, or "no new commit — pushed existing">
Branch: main → origin/main
Files changed: <count>
```
