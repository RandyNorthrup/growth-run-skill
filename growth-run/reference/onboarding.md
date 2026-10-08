# Onboarding a new owner

Run this once per person or project before any posting. Ask the questions in small batches with AskUserQuestion where there are clear options, and in plain text otherwise. Don't guess anything that will be published under their name.

## Intake interview

**1. Identity and voice**
- Name, and the name they post under. Use they/them unless they state their pronouns.
- A one-line bio, plus what they actually do: job, background, years of experience. Record only what they state.
- Time zone, and good hours to post.
- Voice: casual, technical, or witty. Any words or topics they never want used.

**2. Accounts**
- Handle on each platform: X, Bluesky, Facebook, Instagram, LinkedIn, plus Threads, Reddit or Hacker News if used.
- Which accounts are personal, with friends and family following, and which are brand accounts. Never trim follows on personal accounts without asking.
- Confirm they are logged in on this machine's Chrome. They do logins, 2FA and captchas themselves.

**3. Content mix**
- The main niche, which should be most of the content.
- Two to four personal interests to mix in lightly so the feed reads as human, for example games or hobbies.
- Projects and products to spotlight: GitHub user or org, product sites and link targets. Agree the promo ratio (default about 1 in 4).
- Big accounts in their niche to engage with, and accounts they asked to keep following.
- **Skip list:** people never to reply to.
- Topics never to mention, and private items such as roadmaps, keys, client names or family details.

**4. Platforms and targets**
- Posts per platform per run; replies count. For example, 75 each.
- Instagram cadence (default 2 a day, 8+ hours apart, scheduled ahead).
- **Facebook groups:** URL or slug of each, which need admin approval, and which they own (no pacing limit). Ask which ones are strict, for example "non-promo only".

**5. Boundaries**
- **Identity and labels:** does the owner want any bot or automated label on their accounts? The default is no labels; the agent acts as their avatar. Explain that the agent will never deny being AI: it skips "are you a bot?" questions and flags them to the owner instead. Record the answer in the profile.
- Budget. The default is $0: no boosts, paid Connects or subscriptions.
- Which actions need their approval: contracts, deposits, new accounts, deleting posts, anything paid.
- Repos and sites are read-only unless they explicitly say otherwise for a specific change.
- Whether they want follows at all. The default is sparing: about 1,000+ follower accounts only, each with a clear reason.

**6. Gig hunt (optional)**
- Services offered, rate floor ("competitive but don't go too low"), contract or full-time, remote or local.
- Resume file path and portfolio URL. Verified facts only, for example "building websites since <year>" if they say so.
- Platforms: LinkedIn Easy Apply, Hacker News "Who wants to be hired?", Contra, Upwork (inbound only if Connects cost money).
- Accounts they authorize creating, and with which login.
- Where to log the pipeline (a sheet or a file).

## Build the fact file

Before writing any post about their projects, read each README with `gh api repos/<o>/<r>/readme -H "Accept: application/vnd.github.raw"` or from the site. Write `project_facts.md` in the run's scratch dir with one paragraph per project: what it is, its stack, verified numbers, and a **Don't claim:** line for anything the README doesn't support. Refresh it each session for fast-moving projects, and treat release numbers and counts as snapshots.

## Save the profile
Choose the agent's persistent memory if it has one (in Claude Code, the project memory directory, with one index line per file). Otherwise use a `growth/` folder in the working directory. That folder is private: never commit it to a public repo.
1. Fill in `templates/profile.md` and save it as `growth-profile-<slug>.md`.
2. Save `templates/run-state.md` as `growth-run-state-<slug>.md`.
3. Copy `templates/groups.tsv` into the working folder and fill it in from the group list.
4. Each later correction from the owner becomes a line in the profile under "Owner corrections", with the date and their words. That is how the recipe learns for this owner.
