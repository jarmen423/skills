---
name: mut-cs-checkin
description: >-
  use this when advising whether to email a MUT Dashboard user, diagnosing
  silence/usage drop, or drafting a founder check-in — diagnose-first,
  draft-only, no Quivly/CRM tool deps
---
# MUT Dashboard CS check-in

Founder-to-gamer check-ins for [mutdashboard.com](https://mutdashboard.com) (Madden Ultimate Team auction / pricing / sets). Forked from Quivly CS judgment (`usage-drop-investigation`, `post-call-followup` tone, `churn-save-plan` stop rules) — **no Quivly MCP, no B2B ARR/QBR/CSM framing**.

**Core principle:** diagnose before any “just checking in.” A generic re-engagement email on an undiagnosed drop burns trust.

**Anti-jobs:** never send email unasked; never invent usage stats; never pitch upgrades/discounts in a check-in unless Josh explicitly asks. Draft only.

## Inputs (ask if missing)

Gather what you can from context Josh provides, connectors he already has (e.g. Gmail, PostHog, Stripe), or a pasted row. Do **not** call Quivly tools or invent equivalent `get-usage` / `search-tickets` / `search-calls` APIs.

Useful MUT signals (use what exists; say what’s missing):

| Signal | Examples |
|--------|----------|
| Silence | days since last login / last app open |
| Auction activity | snipes, listings, sales viewed, alerts fired |
| Binder / account link | EA account linked?, binder sync freshness |
| Sets workflow | sets calculator use, set builds started/finished |
| Plan / billing | free vs paid, trial end, failed payment |
| Support friction | recent emails, bug reports, refund asks |
| Seasonality | Madden content drop, promo, holiday quiet |

If evidence is thin, say so — do not fake a diagnosis.

## Diagnose first (before drafting)

1. **Shape of the quiet/drop** — sudden cliff vs gradual slide; which signals moved; one user vs a cohort.
2. **Match a primary pattern** (pick one; confidence high/medium/low):

| Pattern | Signature | Check first |
|---------|-----------|-------------|
| **Technical** | Sudden stop after it worked | Outage, login/link failure, platform (Xbox/PS/PC) issue, sync broken |
| **Life / season** | Recurring quiet (work, school, new game mode) | Same calendar window last year / post-promo lull |
| **Value gap** | Never went deep; shallow use then fade | Onboarding incomplete, binder never linked, no first snipe/set win |
| **Displacement** | Gradual leave for another tracker/tool | Mentions of alternatives in mail; feature they asked for missing |
| **Frustration** | Drop after a bad moment | Chargeback, failed trade action, wrong price, support thread |
| **Happy quiet** | Paying / still lightly active, just not chatty | Don’t poke every quiet week |

3. **Recommended play** matched to cause — technical fix ≠ “you ok?” ≠ leave-it-alone seasonal. Wrong play burns trust.

## Should you email?

Decide **yes / no / wait** with one-line why.

- **no** — happy quiet, seasonal, emailed recently, or two unanswered check-ins already
- **wait** — need one more signal (e.g. confirm binder sync vs true churn) before sounding the alarm
- **yes** — clear pattern + a specific ask that helps them (or gets you a useful reply)

### Stop conditions (from Quivly save-plan, adapted)

- Two check-ins with no reply → **stop**. Next is a different channel or graceful leave — not a third nudge.
- Cap contact: don’t stack a check-in on top of a product blast the same week.
- No invented urgency, discounts, or “we miss you” guilt.

## Draft voice (when decision is yes)

Write in **Josh’s first person**, short, warm, specific. Reference one real observation. One easy question. Make reply effortless (“even two words”).

Do:

- Subject like `quick check-in` or `you still sniping?` — human, not marketing
- Name the observation: quiet stretch, binder stale, sets unused, etc.
- Offer a real help path if technical/frustration (reply comes to Josh)

Don’t:

- Feature dumps, upgrade pitches, fake urgency
- “Just checking in” with no observation
- CSM / ARR / QBR / champion / seat language
- Soften bad news in the *internal* diagnosis section (keep drafts customer-facing positive and concrete)

### Example shapes (adapt; don’t copy blindly)

**Silence after real use:**
> Hey {name} — Josh here. Noticed things went quiet on MUT Dashboard after you’d been {sniping / building sets}. Sometimes that’s just life; sometimes something broke or got confusing. Either way, reply works — even “all good” or “X is annoying.”

**Value gap / never activated:**
> Hey {name} — saw you signed up but never got a first {snipe / binder sync / set build} over the line. Want a 60-second nudge for the fastest win, or is MUT Dashboard just not the fit right now?

**Technical suspicion:**
> Hey {name} — usage fell off around {date}. If login, EA link, or prices looked wrong, tell me what you hit and I’ll dig in.

## Output format (always)

**User:** {name or email / id}

**Signals used** — bullet list (and what’s missing)

**Pattern** — {name} · confidence {high/med/low} · one-line evidence

**Should email?** — **yes / no / wait** — why

**If yes — draft**
- Subject:
- Body: (send-ready, first person)

**If no / wait** — what to watch next / when to revisit

## Self-check

- Draft exists but pattern is empty → you skipped diagnose; delete the draft and diagnose.
- Draft pitches a plan upgrade → strip it unless Josh asked.
- Third unanswered nudge → refuse and cite stop conditions.
- Any Quivly tool name (`get-usage`, `search-tickets`, `get-call-summary`, `quivly-tools`, etc.) appears in your plan → remove it; use Josh’s data or ask.
