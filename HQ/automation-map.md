# Automation Map — Recap, Morning Briefing & Weekly Planner

> How the three scheduled agents fit together, and why the system is split
> across Nick's Mac (local) and the cloud. Reference doc — updated when the
> automation topology changes. Last updated 2026-07-22.

The single most important thing to understand: **some jobs run locally on
the Mac (via launchd, so they only run while the Mac is awake), and the
morning briefing runs in the cloud (so it always runs, but cannot see local
files).** Notion is the bridge that carries data from the local jobs to the
cloud briefing.

```
        LOCAL  ·  launchd jobs on Nick's Mac  (only run while the Mac is awake)
 ┌────────────────────────────────────┬───────────────────────────────────────┐
 │  RECAP   (learning-log agent)       │  PLANNING-DIRECTOR  (weekly planner)   │
 │  run-recap-auto.sh · nightly 23:55  │  run-planning-director-*.sh            │
 │                                     │  morning 07:03   ·   evening 21:07     │
 │  reads : session-log.md,            │                                        │
 │          transcripts, log.md        │  morning → writes today's ranked plan  │
 │  writes: log.md  (canonical)        │  evening → reconciles what got done    │
 │  heartbeat → recap-cron.log         │                                        │
 └──────┬────────────────┬─────────────┴─────────────────┬──────────────────────┘
        │ append         │ mirror each                    │ read + write
        │ (source of     │ recapped day                   │ the plan
        ▼  truth)        │                                │
   ┌──────────┐          │                                │
   │  log.md  │          │                                │
   └──────────┘          │                                │
 ═══════════════════ LOCAL ══╪════════════════════════════╪══ CLOUD ════════════
                             ▼                            ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │                              NOTION   (cloud)                               │
 │     ┌───────────────────────┐            ┌───────────────────────────┐     │
 │     │  Learning Log DB       │            │  Weekly Task Planner       │     │
 │     │  1 row per day         │            │  + Tasks Tracker           │     │
 │     └───────────┬───────────┘            └─────────────┬─────────────┘     │
 └─────────────────┼──────────────────────────────────────┼───────────────────┘
                   │ yesterday's row                       │ today's Deep Work
                   │ → "Yesterday, You Learned"            │ + Job Prep
                   ▼                                       ▼  → "Today's Plan"
 ┌───────────────────────────────────────────────────────────────────────────┐
 │   MORNING BRIEFING   ·   cloud task   (NOT launchd)                         │
 │   fires ~08:09 ET  →  runs even if the Mac is asleep                        │
 │                                                                            │
 │   also reads:  Gmail  ·  Google Calendar  ·  GitHub origin/main (HQ memory)│
 │   ✗ cannot see local files — everything it needs must be on Notion or      │
 │     pushed to GitHub                                                        │
 │   output:  composes the digest  →  emails it to Nick                       │
 └───────────────────────────────────────────────────────────────────────────┘
```

## Daily timeline (Nick's local time, ET)

```
  07:03  ── planner (morning) writes today's plan ─────────────►  Notion
  08:09  ── briefing reads Notion + Gmail + Calendar ──────────►  emails Nick
             • Today's Plan   ← plan written at 07:03 this morning
             • Yesterday, You Learned  ← recap mirrored at 23:55 last night
  21:07  ── planner (evening) reconciles what actually got done
  23:55  ── recap writes log.md + mirrors the day ─────────────►  Notion
```

## Why it's shaped this way

- **Local jobs (recap, planner)** run via launchd and only fire while the
  Mac is awake — that's what the 23:50 scheduled wake (`pmset repeat
  wakepoweron`) + overnight AC power protect.
- **The briefing runs in the cloud**, so it always fires *but can't read the
  Mac's files*. That was the original "Yesterday, You Learned" bug: the
  recap wrote `log.md` locally, and the cloud briefing never saw it.
- **Notion is the bridge.** Both local jobs publish to Notion; the cloud
  briefing reads from Notion. `log.md` stays the canonical store, and the
  Learning Log DB is its mirror purely so the briefing can reach it.

## Component reference

| Piece | Kind | Trigger | Key file / surface |
|---|---|---|---|
| Recap | Local launchd | nightly 23:55 ET | `run-recap-auto.sh` → `log.md` + Learning Log DB |
| Planning-director | Local launchd | 07:03 & 21:07 ET | `run-planning-director-*.sh` → Weekly Task Planner + Tasks Tracker |
| Morning briefing | Cloud task | ~08:09 ET (05:09 PT server clock) | reads Notion + Gmail + Calendar + `origin/main`; emails Nick |
| Learning Log DB | Notion (cloud) | — | `collection://e0fa7eac-d4e3-4c17-aaa1-8ada7081c6b7` |

⚠️ Timezone note: the briefing runs on Pacific-clock servers (~05:09 PT =
~08:09 ET). The recap writes each row's date in ET; the briefing computes
"yesterday" in PT. Around midnight/DST boundaries they can disagree by a day
— worth watching, not currently a problem.
