# Content

## Voice
- Write in the owner's voice: plain, specific and confident. Use short sentences and no hype words.
- Prefer one concrete fact or mechanism over adjectives: "Rancor returns to hand every time" beats "Rancor is amazing".
- Keep personal angles to what the owner has stated. Otherwise ask a question ("Did X or Y make the bigger difference?").
- No emoji spam and no hashtag walls. Use one or two relevant tags only where the platform rewards them (Instagram captions).

## Fact file (`project_facts.md`)
- Keep one paragraph per project, built from the README: what it is, its stack, the verified numbers, and the live URL.
- Add a **Don't claim:** line for tempting but unsupported claims, such as unreleased features, wrong platform labels ("not a VS Code extension") or merged-upstream status.
- Re-check fast-moving facts each session: latest release, counts, what was tested. Label numbers as snapshots.

## Post bank (`bank.tsv`)
- The format is `key<TAB>text<TAB>optional link`.
- Run `python bank.py check` to flag posts over X's 280 weighted characters or Bluesky's 300.
- `python bank.py x <key>` and `python bank.py b <key>` print intent URLs.
- Write a mix:
  - **About 50%: organic niche takes.** Rules of thumb, lessons, reactions to the day's news, and questions to the audience.
  - **About 25%: project spotlights,** leading with the distinctive feature.
  - **About 15%: questions and polls.** Questions get replies, and replies get reach.
  - **About 10%: personal interests mixed in** (the owner's hobbies), ideally tied back to the niche. For example: "a Commander deck is dependency management", or "a type chart is a lookup table, not an if/elif wall".
- Link-free posts get more reach on X. Put a project link in the post only when it's the point, or in a reply.

## Replies that earn follows
- Answer what was said. Add one useful fact, angle or experience the owner actually has.
- End with a question when it fits; it invites a second exchange.
- With big accounts, be early, specific and short. A crisp, correct take under a big post is the cheapest growth there is.
- Never "Great post!", never flattery-only, never a pitch.

## Instagram carousels
- 8 slides, 1080×1350 (4:5). The hook slide states the payoff. Each later slide carries one idea, and the last slide is a takeaway or CTA.
- **Rotate visual identity every post.** Never reuse the last 2–3 styles. Style ideas:
  - cream paper editorial (serif display + grotesk)
  - ops dashboard (near-black grid, mono)
  - risograph (pastel overprint)
  - Swiss poster (heavy grotesk, one accent)
  - notebook (hand-drawn)
  - CRT terminal (green on black)
  - darkroom (red safelight)
  - blueprint (cyan grid)
  - synthwave (gradient + chrome)
  - gauges or instruments
  - brutalist black and yellow
- Vary the structure too: big numbers, diagrams, checklists, code-first slides, quote cards.
- Use Google Fonts through `<link>` and render with `--virtual-time-budget=6000` so the fonts load.
- Put the handle on every slide. Captions go in `<name>-caption.txt`: a hook line, 3–5 lines of value, a question, and a few tags.
- Track `name → style → date` in the run-state memory.
