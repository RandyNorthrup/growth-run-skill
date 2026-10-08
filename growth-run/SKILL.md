---
name: growth-run
description: Run an owner's social-growth and freelance-gig operation end to end. It onboards a new person or project, then runs posting and replying rounds on X, Bluesky, Facebook groups and Instagram, and checks in on web-dev or freelance job hunting, all under the owner's standing rules and anti-spam pacing. Use when asked to "set up growth for <person/project>", "do a posting and responding run", "reply to everyone", "N posts per platform", "schedule Instagram carousels", "post in the Facebook groups", or "check in on the job hunt".
---

# Growth Run

This skill is the recipe for a combined **social growth loop** and **gig hunt**, run through the owner's own logged-in browser. It supplies the process, rules and tooling. Each owner's profile supplies the content: who they are, their topics, projects and groups. It follows the open Agent Skills layout, so any agent that can read files, run Python and drive a browser can use it.

## 0. First: load or create the owner profile

Look for `growth-profile-<slug>.md` and `growth-run-state-<slug>.md`. Check the agent's persistent memory first. If the harness has no memory, look in a `growth/` folder in the working directory.
- **Found:** read both and continue from the run state.
- **Not found:** run onboarding first (`reference/onboarding.md`, template `templates/profile.md`).

Use one profile per person or project, and never mix their content.

## 1. Setup (once per machine)

1. Run `python scripts/doctor.py`. It checks Python, Chrome, a silent clipboard round-trip and the public APIs, then prints READY or what to fix.
2. Set up the browser tool. **Proven:** the chrome-control MCP driving the owner's real logged-in Chrome. Other tools need the capabilities in `reference/browser-ops.md` and are untested.
3. The owner logs in to each platform in that browser, and handles 2FA and captchas themselves.
4. Make a working folder for the run, and copy `templates/log.tsv`, `templates/bank.tsv` and `templates/groups.tsv` into it.

## 2. Rules: read `reference/rules.md` every session

They override convenience. In short:
- The owner's **repos and sites are read-only**. **Budget is $0** unless they say otherwise.
- **No cold email.** The owner approves every contract and deposit.
- **Never invent** first-person facts. Every project claim matches the README.
- **Never deny being AI, and never claim to be human.** Skip bait and flag it to the owner.
- **Follow sparingly.** The goal is gaining followers, not following.
- **About 1 in 4 posts** is self-promotion. Organic replies carry no links.
- **Pace Facebook groups** with `pace.py`. Admin-approval groups get at least 6 hours, never back-to-back.
- **Never touch the owner's tabs.** Announce any native dialog. Use one browser worker at a time.
- **Run silently.** Helpers never pop console windows; use the Python scripts, not ad-hoc PowerShell or cmd.
- **Ask before infrastructure fights** such as credentials or settings that live only in a dashboard.

**Anti-spam is the whole game:** read `reference/anti-spam.md` (content, timing, approval-queue traps, stop signals) and `reference/gotchas.md` (everything that broke before).

## 3. The round loop (`reference/run-loop.md`)

1. **Replies first** on every platform. Respond to everyone except the skip list, jabs, bait and gibberish.
2. **Proactive replies** on niche leaders' fresh posts. This is where new followers come from.
3. **Original posts** from the post bank: mostly organic niche content, about 1 in 4 project spotlights, and a few personal interests.
4. **Instagram:** render carousels, each in a unique visual style, and schedule them ahead at about 2 a day.
5. **Facebook groups:** post only to groups that `pace.py` marks READY, then `--mark` each one.
6. **Log every action** to `log.tsv`. Run `tally.py` against the targets. Update the run state at milestones.
7. **When the targets are met,** do the gig-hunt check-in (`reference/jobs.md`).

Post a one-line status between batches. Inside the rules, don't stop for approval.

## 4. References (load only what you need)

| File | What it covers |
|---|---|
| `reference/onboarding.md` | Intake interview, fact file, saving the profile |
| `reference/rules.md` | Standing rules with reasons |
| `reference/anti-spam.md` | Content and timing that looks human; approval-queue traps; when to stop |
| `reference/gotchas.md` | Hard-won failure modes by area |
| `reference/run-loop.md` | Session start, rounds, cadence, memory, end-of-run report |
| `reference/content.md` | Voice, fact file, post bank mix, reply craft, carousel styles |
| `reference/platform-x.md` | Intent-URL posting, context, images, limits |
| `reference/platform-bluesky.md` | Public API discovery, reply flow, clipboard images |
| `reference/platform-facebook.md` | Pacing, group posts, big comment threads |
| `reference/platform-instagram.md` | Rendering, scheduling, replies, the silent throttle |
| `reference/jobs.md` | LinkedIn guest API, Easy Apply, HN, Contra, Upwork inbound |
| `reference/browser-ops.md` | Browser tool requirements, tabs, snapshots, clipboard, recovery |

## 5. Scripts (`scripts/`, Python 3.8+, standard library only, silent)

| Script | Purpose |
|---|---|
| `doctor.py` | Setup check (run first on a new machine) |
| `clip.py <file> [n]` / `--text s` | Copy a whole file or line *n* to the clipboard, verified. Uses the Win32 API, so no window pops up |
| `clipimage.py <img>` | Image to the clipboard, for pasting into Bluesky or Contra |
| `xintent.py <id\|0> "text"` | X reply or post intent URL plus weighted length |
| `xthread.py <id>` | X post text and what it replies to |
| `xsynd.py <hours> handles…` | Fresh originals from X accounts |
| `bsky_open.py <owner>` | Unanswered replies on the owner's Bluesky threads |
| `bsky_authors.py` / `bsky_feed.py` → `bsky_filter.py <owner>` | Fresh Bluesky posts worth replying to, minus ones already answered or gated |
| `bank.py check\|x\|b\|text` | Post bank length checks and intent URLs |
| `pace.py groups.tsv [--mark slug]` | Facebook group pacing guard (READY or wait, and why) |
| `fb_snap.py <snapshot-file>` | Map Facebook commenters to their Reply and View-replies refs |
| `render_carousel.py` | Headless Chrome HTML to 1080×1350 slides (private profile, no window) |
| `li_search.py` / `li_detail.py` | LinkedIn jobs through the guest API |
| `tally.py log.tsv x=75,b=75` | Progress against the targets |
| `wait_cpu.py [pct]` | Wait out CPU spikes before heavy pages (run in the background) |
| `bridge_wait.py` | chrome-control only: wait for the bridge to come back after a drop |

Templates: `profile.md`, `run-state.md`, `groups.tsv`, `bank.tsv`, `log.tsv` and `carousel.html`.
