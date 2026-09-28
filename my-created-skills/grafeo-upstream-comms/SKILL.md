---
name: grafeo-upstream-comms
description: How to explain, discuss, and plan Grafeo upstream contribution work with Josh (jarmen423) — splitting PRs for GrafeoDB/grafeo, mapping #393 pieces to GitHub issues, bot review findings, the agentmemorylabs fork and the AMH pin, and editing the plan in agent-memory-hosted/.hermes/plans/grafeo-upstream/PLAN.md. Use this whenever the conversation touches GrafeoDB/grafeo upstream, StevenBtw, PR #393 or its split (S1, S2...), cubic-bot findings, ~/code/grafeo-upstream, or whether a fix also belongs in our fork — even for a quick question like "what is S1" or "is this in our fork".
---

# Grafeo upstream: how to explain, discuss and plan

Grafeo upstream work involves several codebases, several kinds of "issue",
and short labels (S1, P1, pin) that are easy to lose track of. Josh has said
plainly when an explanation confused him and when one helped. This guide
collects those moments so the next session starts in the shape that works.

## The world, and the words for it

Use these terms the same way every time, and say which one a claim is about:

| Say | Means |
|---|---|
| **upstream/main** | `GrafeoDB/grafeo` main (StevenBtw's repo). Split PRs target this. |
| **the #393 branch** | `agentmemorylabs:diagnostics/lpg-memory-accounting`, head of GrafeoDB/grafeo#393 |
| **the fork pin** | `agentmemorylabs/grafeo` at the commit AMH depends on (`e0ff9bc8` as of 2026-09-28) |
| **personal fork** | `jarmen423/grafeo`, the only push target for upstream PRs |
| **GitHub issue** | A numbered upstream issue (#401, #389, #462, #450) |
| **#393 review comments** | The cubic-bot findings on #393 plus bugs the owner flagged there. Never call these just "issues". |
| **S1, S2...** | One planned split PR each. Every S-number has its own heading in PLAN.md. |
| **P1/P2/P3** | cubic-bot severity. Say "P1 (the bot's most serious level)" the first time in a conversation. |

## Principles, each with the moment it came from

### 1. Answer in the frame the question was asked
If Josh offers categories, the first line picks one (or says "partly each")
before any evidence. If he gives an if/else instruction, check the facts,
then say which branch applied and why.

> Josh: "is this a bug we already fixed that's in our PR, or a bug we started
> fixing but needs more work to land? or is it a bug we're introducing?"
> Good first line: "It's partly each. The bug was already in upstream, #393
> contains a partial fix, and that partial fix creates a new bug of its own."
> Then one short section per category.

> Josh: "if it's going to be its own PR [do X]; if it's the PR that responds to
> #450 [do Y]..." → check #450 and the owner's comment first, then open with:
> "#450 is the owner's epic to replace the whole store. S1 doesn't respond to
> it... So S1 gets its own section at the top."

### 2. Say where every claim is true
"Present", "fixed" and "never addressed" mean nothing until you name the
place: upstream/main, the #393 branch, the fork pin, or local uncommitted work.

> Earlier reply: "The review bot's findings were mostly never addressed."
> Josh: "never addressed on our fork or the PR branch?"

### 3. Say how strong every claim is
Keep these levels separate and name the one you actually reached:
1. the code is there (grep or blame)
2. a test fails on it
3. AMH can reach it (a feature is enabled, a caller exists)

Don't turn level 1 into "this affects AMH". If you overstated something,
say so plainly and restate it at the level you really reached.

> Josh: "To be clear, you are asserting that the P1s need fixing both on our
> current fork and the PR branch?"
> Good reply: "No. I overstated it earlier. Here's what I actually
> established..." followed by a per-finding table of what was checked.

### 4. Define every label, and give each one a home
Never use S1, a commit SHA's role, "held", "dropped" or "the pin" without it
being defined, either in the plan or the first time it comes up. In PLAN.md,
every S-number gets its own heading, in PR order. A label that only lives in
a sub-bullet of another section gets lost.

> Josh: "what is S1" → "the plan skips straight to S2..." (S1 was buried
> under the #450 "dropped" section).

### 5. Give provenance for every piece
For each piece of code, say whose it is (ours, StevenBtw's, or GitHub's
"Update branch" merge), which commit it comes from, and whether it's taken
whole or in part. Josh's goal in his own words: "split this into
identifiable pieces, clear provenance."

### 6. Every upstream item gets a fork line, and the default is "port it"
For each item, answer: is the bug in the fork pin, does AMH use that code
today, and so will we fix it in the fork? He asked this unprompted ("Do issue
fixes also need to be added to our fork?"), so answer it before he has to ask.

The default: **if a fix is good enough to send upstream and the bug is in
the pin, it goes to the fork too**, even when AMH doesn't use that code
today. "Nothing we run triggers it" isn't a reason to skip it on its own.
Josh: "if we leave bugs that might be relevant, that's also messing up our
fork... we spent all this time doing work to fix it, but we didn't port it
because we're not using it today, but maybe we will be." Skip only fixes to
features we'd realistically never use, and name the feature when you do.
Fork fixes still go on a separate fork branch, with a test that fails on the
pin, and only with Josh's OK.

When describing a bug, keep "whose code has the bug" separate from "who
found or fixed it". The point-get bug was StevenBtw's code that the fork
inherited. It wasn't "a bug in our code that we fixed upstream but not in
the fork", which is how the old wording read to him.

### 7. Lead with what's new, then how it works and why
When a change adds something, say so before anything else, in plain words:
"adds a new function, `get_compressed`", then what it does and why it's
needed. Someone reading the plan without the code can't tell a new function
from an existing one, and "Parts: the `get_compressed` hunk" reads like
something that was already there.

> Too thin: "Parts: the `get_compressed` hunk of `195678c3` (binary search
> on `index_to_id`...)."
> Better: "Adds a new function, `get_compressed`, taken from `195678c3`.
> `get` calls it when a value isn't in uncompressed storage. It
> binary-searches the sorted id list to find the value's position, then
> reads it out..."

The same goes for anything the plan excludes or defers. Say where it came
from (which commit, whether a reviewer flagged it) and why it's out. A bare
"excludes the spill-restore `or_insert` change" left Josh asking where that
came from and why it was mentioned at all.

### 8. Plain words over jargon
Say "the bug is there, but nothing we run triggers it today", not "latent".
Say "deleted values come back", not "resurrects removed values". If a
technical term is the right one, define it in the same sentence the first
time: "a trailer (a `Key: value` line at the bottom of a commit message)".
Josh reads the plan cold, sometimes before the code, so every term has to
make sense there.

### 9. Stay on the thread, and put corrections first
A tangent that adds a new worry (a merge commit, a "dropped API" that turned
out to be wrong) is what led to "I'm kinda confused." If a link or detail
needs no action, say that first. If you got something wrong earlier, start
with "Correction first: ...", then continue.

### 10. Be concrete about locations and what he'll see
- Give file paths as clickable links. "what is the path to the PLAN.md file"
  should never need asking; link the file whenever you mention it.
- Say what will actually appear. Josh: "those are links to github, I don't
  see [the clickable card you mentioned]." Don't promise a UI element (a
  card, button or panel) you haven't confirmed will appear.
- For work in progress, say where it lives: uncommitted, committed locally,
  pushed to the personal fork, or PR opened.

## PLAN.md shape

Josh's structure, which he confirmed "was very helpful":

> "each top level item should be the per-(github)-issue map and nested items
> should include parts of that issue/PR (just brief high level) + any comments
> from #393 reviewers that belong there + a mention, if something is not
> already in our fork, of whether we will/should also commit/merge it there"

```markdown
### S1 <short name> (standalone | GitHub issue #N) → first PR
- Why / what the issue asks: one line, quoting the owner if he asked for it
- Parts: lead with what's added ("adds a new function, `x`") or changed, then
  what it does and why; then the source commit(s), whole or partial
- Additional work beyond <the issue | the #393 hunk>: only if the PR carries more
- Not included: anything nearby that's left out, where it came from, and why
- Review comments: #393 findings placed here by `git blame`, one line each
- Status: where the work lives (uncommitted / local commits / pushed / PR #)
- Fork: whose code has the bug? in the pin? used by AMH today? → port to fork
  (default) or skip (only for a feature we'd never use; name it)
```

Ordering and placement:
- The PR that goes out first goes at the top. A standalone PR (no GitHub
  issue) gets its own section. Don't nest it under the issue its code
  happens to come from.
- If a PR carries more than its issue asks, add an explicit sub-bullet
  "Additional work beyond <issue>".
- Work that's not going upstream still gets listed: a "dropped" section
  (owner replaces it) and a "held / not mapped" section, so every #393
  commit and review comment has a place.
- Keep S1-specific notes in S1's section, not scattered through the
  Handoff and Log.

## Reply shape that worked

The per-issue answer Josh called "very helpful" looked like this. Copy the
shape, not the content:

```markdown
**1. #401: vector index restore (S2)**
- Issue asks: vector **and text** indexes survive close/reopen
- From #393: `7a13c6d2`, `75e4c658`
- Review fixes riding along: rehydrate deadlock (P1); stale data after empty rehydrate; ...
- Gap: we only restore vector indexes. The PR should say "Part of #401".
- Fork: already in the pin; AMH uses vector indexes → test each finding on the pin.
```

End status replies with what's waiting on Josh ("S1 is waiting on your diff
review; nothing is committed or pushed"). Nothing goes to GitHub (pushes,
PRs, issue comments) without his explicit OK.
