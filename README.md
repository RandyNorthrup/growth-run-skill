# growth-run

**An agent skill that runs a person's social growth and freelance gig hunt from their own browser, under strict anti-spam rules.**

You give an AI coding agent (Claude Code, Codex, or any agent that can read files, run Python and drive a browser) this skill. It then:

- **Onboards** a person or project: identity, voice, accounts, topics, projects, Facebook groups, targets and boundaries.
- **Runs posting and replying rounds** on X, Bluesky, Facebook groups and Instagram. It replies first, adds original posts in the right mix, schedules Instagram carousels in varied styles, and keeps a steady flow in groups.
- **Paces everything like a person would.** Admin-approval groups are spaced out, Instagram's silent comment throttle is respected, and follow limits are kept.
- **Checks in on the gig hunt:** LinkedIn guest-API search and Easy Apply, the Hacker News hiring thread, Contra, and Upwork (inbound only).
- **Logs every action**, tallies it against the targets, and keeps a resumable run state.

The process and rules are generic. Everything personal lives in a per-owner profile that the agent creates during onboarding, so one skill serves many people.

> Status: the process was used in production in October 2026 with the chrome-control MCP driving a real logged-in Chrome. The other browser tools listed below should work but are untested.

---

## Quick start

```bash
git clone https://github.com/RandyNorthrup/growth-run-skill.git
cd growth-run-skill
python growth-run/scripts/doctor.py   # checks Python, Chrome, a silent clipboard round-trip and the public APIs
```

Install the `growth-run/` folder where your agent looks for skills:

| Agent | Install |
|---|---|
| **Claude Code** | Copy or symlink `growth-run/` to `~/.claude/skills/growth-run/` (all projects) or `<project>/.claude/skills/growth-run/` |
| **Codex CLI** | Copy it to your Codex skills directory (for example `~/.codex/skills/growth-run/`). See your Codex version's skills docs |
| **Other agents** (Gemini CLI, Cursor, Aider and so on) | Keep the folder anywhere, and tell the agent: "Follow `growth-run/SKILL.md` for this task." The skill is plain Markdown plus Python and has no vendor-specific dependencies |

Then ask your agent:

```text
Set up growth-run for me. I'm <name>; my niche is <topic>; my projects are on github.com/<user>.
```

It runs the intake interview, builds a fact file from your READMEs, and saves your profile. After that:

```text
Do a posting and responding run: 50 per platform, replies count. Then check the job hunt.
```

---

## Requirements

- **Python 3.8+.** The scripts use the standard library only. Pillow is optional, for silent image copies on Windows.
- **Google Chrome**, with the owner logged in to each platform. The owner handles logins, 2FA and captchas.
- **A browser-control tool** for the agent:
  - **Proven:** [chrome-control MCP](https://github.com/RandyNorthrup/chrome-control-mcp), which drives your real Chrome visibly and gives each session its own tab.
  - **Should work (untested):** Playwright MCP in a mode that attaches to your real, logged-in profile, or the Claude in Chrome extension. To qualify, a tool must be able to:
    - drive the real logged-in profile, headed
    - read page text
    - give element refs
    - click by ref and by coordinates
    - press keys
    - take screenshots
    - upload to file inputs
    - paste from the system clipboard

    See [`growth-run/reference/browser-ops.md`](growth-run/reference/browser-ops.md) for the capability table.
- **Optional:** the `gh` CLI, used only to read READMEs for the fact file.

**Platforms:** Windows, macOS and Linux. The clipboard uses the Win32 API on Windows (silent, no PowerShell windows), `pbcopy` on macOS, and `wl-clipboard` or `xclip` on Linux.

---

## Why it doesn't look like a bot

The rules in [`anti-spam.md`](growth-run/reference/anti-spam.md) and [`rules.md`](growth-run/reference/rules.md) are the core of this project.

**Content**
- Replies are specific to the post and never generic praise. They are rewritten per platform, never pasted around.
- Self-promotion is about 1 in 4. Organic replies carry no links.
- Every product claim is checked against the README. The agent never invents first-person facts, never claims to be human, and skips "are you a bot?" bait rather than arguing.

**Timing**
- Actions are spread across the day. Instagram gets about 2 posts a day, 8+ hours apart. X follows stay under the rate limit.
- `pace.py` enforces Facebook group cooldowns:
  - Admin-approval groups get 6+ hours since that group's last post, one per round, and never two back-to-back.
  - Groups with a stuck pending post are skipped.
  - The owner's own groups can post freely.

**Silent failures it watches for**
- Instagram drops comment replies without an error after a burst.
- Pending approval posts are invisible, which invites duplicates.
- Stale element refs, and a bridge that drops when the machine is busy.

**Hard stops:** rate-limit or "action blocked" toasts, removed posts, captchas, and anything paid, irreversible or contractual. The agent stops and asks the owner.

---

## What's in the box

```
growth-run/
  SKILL.md                entry point the agent reads first
  reference/              rules, anti-spam, gotchas, run loop, content, one playbook per platform, jobs, browser ops
  scripts/                standard-library Python helpers (silent; no console windows)
  templates/              profile, run state, groups.tsv, bank.tsv, log.tsv, carousel.html
tests/                    offline tests for the scripts (run in CI on Windows, macOS and Linux)
```

| Script | Purpose |
|---|---|
| `doctor.py` | Setup check |
| `clip.py`, `clipimage.py` | Verified, silent clipboard for text and images |
| `xintent.py`, `xthread.py`, `xsynd.py` | X: intent URLs, thread context, fresh posts from chosen accounts |
| `bsky_open.py`, `bsky_authors.py`, `bsky_feed.py`, `bsky_filter.py` | Bluesky: unanswered replies and fresh posts to engage with, through the public API |
| `bank.py` | Post bank: length checks for X and Bluesky, and intent URLs |
| `pace.py` | Facebook group pacing guard |
| `fb_snap.py` | Map commenters to their reply buttons in large saved snapshots |
| `render_carousel.py` | HTML to 1080×1350 Instagram slides with headless Chrome (private profile) |
| `li_search.py`, `li_detail.py` | LinkedIn jobs through the guest API (no login) |
| `tally.py` | Progress against the per-platform targets |
| `wait_cpu.py`, `bridge_wait.py` | Wait out CPU spikes, and recover the chrome-control bridge |

Run the tests with `python -m unittest discover -s tests -v`.

---

## Privacy

- Owner profiles, run state, logs and drafts belong in the agent's private memory, or a `growth/` working folder that `.gitignore` excludes. **Never commit them.**
- The skill never writes to the owner's repos or sites, never spends money, never cold-emails, and never accepts contracts or deposits without the owner's approval.

## Contributing

Issues and PRs are welcome, especially:
- playbooks for more platforms (Threads, LinkedIn posting, Reddit)
- verified mappings for other browser tools
- new gotchas, each with how it was found and the fix

Keep scripts standard-library only and silent, and add a test for any logic.

## License

MIT. See [LICENSE](LICENSE).
