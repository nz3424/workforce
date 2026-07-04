# morning-briefing — Agent Memory

> This file is the persistent memory for the Morning Briefing agent.
> Read it on startup (after HQ/CLAUDE.md).
> **Do NOT write to this file during or after a run.** There is no run log. Do not create one.

---

## Learned Preferences

<!-- Things Nick has corrected, adjusted, or praised. Add entries as patterns emerge. -->
<!-- Format: Date — Observation -->

- Default to short. Nick will ask for more if needed. No walls of text, no lengthy preambles.
- No emoji anywhere in output.
- No filler phrases ("good morning!", "here's your daily digest", etc.) — open directly with content.
- Lead with what requires action or a decision; push passive FYI items to the bottom.

---

## Recurring Context

<!-- Standing facts that affect how the briefing should be produced. -->

- **Deep work window:** 10:00 AM–12:00 PM is protected for focus work. Flag any meetings scheduled in this window as [DEEP WORK IMPACT].
- **Weekly review:** Every Sunday — don't flag Sunday as unusual if calendar is light.
- **Life stage:** Nick just graduated and is starting a new SWE job (May 2026). Anything job-related (onboarding, manager comms, colleague threads) is high-priority for the first 90 days.
- **Standing blocks:** None defined yet — update this section once Nick's recurring meetings are established at his new job.
- **Contacts file:** Check `HQ/contacts.md` before flagging emails that need replies — use tone profiles there to assess urgency and context.
- **Gmail send auth:** Automated sending uses a **production Desktop** OAuth client ("Morning Briefing Desktop", project *Google Workspace MCP*) via `GMAIL_CLIENT_ID` / `GMAIL_CLIENT_SECRET` / `GMAIL_REFRESH_TOKEN` env vars in the Morning Briefing cloud environment. Because the app is in production, the refresh token is long-lived — it only dies on a Google password change or manual revoke, never on a schedule.

---

## Ops History

<!-- Human-added maintenance notes. The agent's "read-only during runs" rule still applies. -->

- **2026-07-03** — Automated send broke (`invalid_grant` on `GMAIL_REFRESH_TOKEN`; briefing fell back to a Gmail draft). **Root cause:** a Google account password change revoked the old Gmail-scope refresh token — a one-time event, *not* the 7-day "Testing" expiry (the OAuth app is in production). **Fix:** created a new **production Desktop** OAuth client "Morning Briefing Desktop" (project *Google Workspace MCP*), re-minted the refresh token, and updated all three `GMAIL_*` env vars in the Morning Briefing cloud environment. Verified by a real briefing delivered to the inbox. **If `invalid_grant` recurs:** check for a recent password change or revoked access first, then re-mint the refresh token under the Desktop client (Desktop type avoids the `redirect_uri_mismatch` that a Web-application client hits in a local loopback OAuth flow).

---

## Open Items

<!-- Things from a previous briefing that still need follow-up, -->
<!-- if not yet captured in HQ/memory.md. -->

*(no entries yet)*
