# /sync — Workforce Git Sync

Sync the Workforce repo to GitHub. Follow these steps exactly:

## Step 1 — Fetch remote
Run `git fetch origin` to pull down the latest remote state without
merging. This makes the comparison accurate.

## Step 2 — Compare local vs. remote
Run the following and report results before doing anything else:

```
git status                        # local uncommitted changes
git diff --stat HEAD origin/main  # commits ahead/behind remote
git log origin/main..HEAD --oneline  # local commits not yet on GitHub
git log HEAD..origin/main --oneline  # remote commits not yet local
```

Report a clear summary in this format:
```
Repo Comparison — local vs. origin/main
  Local uncommitted changes: <N files, or "none">
  Commits ahead of GitHub:   <N, or "none">
  Commits behind GitHub:     <N, or "none">

  Unpushed commits:
    <hash> <message>   ← only if ahead
    ...

  Remote-only commits:
    <hash> <message>   ← only if behind
    ...
```

## Step 3 — Handle divergence
Before staging anything, check for conflicts:

- **Behind only (no local changes, no unpushed commits):** Run
  `git pull origin main` and report "Pulled N commits from GitHub. Up to date."
  Then stop — nothing to push.

- **Behind AND have local changes or unpushed commits:** Stop and warn:
  "Local and remote have diverged. Pull first or resolve manually before
  syncing." Do not commit or push. Describe exactly what would conflict.

- **Ahead only or clean divergence (no conflicts):** Continue to Step 4.

- **Clean (nothing to commit, nothing to push):** Report
  "Repo is clean — already in sync with GitHub." and stop.

## Step 4 — Stage changes
Run `git add -A` to stage all local changes.

## Step 5 — Generate commit message
Categorize staged changes into:
- **Structural** — agent specs, TEAM.md, CLAUDE.md, HQ files, .gitignore, new agents
- **Memory** — any file named `memory.md` or in `outputs/` or `drafts/`

Build the commit message:
- **Only memory files:** `Update agent memory — [YYYY-MM-DD]`
- **Only structural:** Describe what changed, e.g. `Add /sync comparison step`
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

If there are only unpushed commits and no new local changes, skip
Steps 4–5 and go straight to Step 6.

## Step 6 — Commit (if there are staged changes)
Run `git commit -m "<generated message>"`.
Skip this step if there were no local uncommitted changes to stage.

## Step 7 — Push
Run `git push origin main`.

## Step 8 — Report
```
Synced to GitHub.
Committed: <commit subject, or "no new commit — pushed existing">
Branch: main → origin/main
Files changed: <count, or "—">
```
