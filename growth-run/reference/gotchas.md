# Gotchas (learned the hard way)

These are grouped by area. Each one cost real time at least once.

## Truth and tone
- **Invented first-person facts get caught.** A reply said "it's what I run in Zed and JetBrains" while the README said JetBrains was untested; the reply was deleted and reposted. "What got so many of us into web dev" drew a "Wow robot…" reply. State only what the owner said.
- **Counts are snapshots.** "26 agents are building it" reads as a fixed fact. Write "a fleet of agents", or "snapshot at 8:30 pm: 26 active".
- **Table-stakes features make weak promos.** Rewind, permission modes and diffs are table stakes; lead with what's unique.
- **Product labels matter.** Calling a multi-editor tool "a VS Code extension" undersells it and annoys the owner. Copy the README's own framing.
- **Word.tld autolinks.** "AGENTS.md" turned into a link and Bluesky built the preview card from agents.md, so the post advertised someone else. Reword file names.

## Duplicates and double-posting
- Check for an existing owner reply ("View all N replies") before replying. One duplicate went out to a comment the owner had answered 22 hours earlier.
- Pending approval posts are invisible to a quick look; check before re-posting.
- After a composer closes, verify on a reload (comment count, or the profile) before retrying. Facebook replies show "Posting…" and blank spinner circles for a while and then land.

## Browser and tool mechanics
- **The owner's active tab is not your tab.** `browser_tabs` "active" is what the owner is looking at. Always drive your own session tab.
- **Subagents share the browser session tab.** Running a browser subagent and the main thread at once hijacks navigation. Do browser work sequentially.
- **`click_at` needs a fresh screenshot,** or it's refused with "page moved". Facebook and Instagram pages scroll themselves after load, so take a screenshot and then click.
- **Screenshot scaling.** Some tools display screenshots scaled (for example 2000 px wide) while `click_at` expects device pixels (2047). If small targets miss, multiply by the ratio, about 1.02.
- **Refs go stale** when the page re-renders ("Unknown element ref"). Re-snapshot, or scroll the target into view and use a screenshot plus coordinates.
- **Snapshots of heavy pages overflow.** They're saved to a file; parse them with a script (`fb_snap.py`). Reading one whole wastes the context window.
- **Tool parameter names:** `press_key` takes `keys`; `wait_for` takes `timeout_ms` and `absent`. Load deferred tool schemas before calling.
- **Escape is dangerous.** It closes Facebook post modals and drafts, and opens "Discard post?" on Instagram. Close popups with their ✕ instead.
- **Hover cards** (profile popups) appear under the pointer and cover buttons. Close them with ✕.
- **Two composers on X:** the hidden file input in the snapshot belongs to the background timeline composer. Upload through the modal's "Add photos or video" ref.

## Clipboard
- On Windows, PowerShell `Set-Clipboard` sometimes leaves the clipboard empty, and every PowerShell call from an agent shell flashes a console window in the owner's face. Use `clip.py` (Win32 API, silent, verified).
- If focus is lost (`focus.tag == body` in the key-press result), the paste went nowhere. Click into the editor and paste again.
- Write post text to a UTF-8 file first. Inline shell quoting mangles apostrophes, quotes and emoji.

## Bridge and machine load
- The browser bridge drops periodically (roughly every 20 heavy actions) and whenever the CPU is pegged. When it happens:
  - **Recover:** wait for a fresh native host, then list tabs. If a tab reports "DevTools attached", close it and open a new one.
- When other work on the machine (builds, linters, agent fleets, antivirus scans) pushes CPU above 90%:
  - **Stop driving heavy pages.** Run `python wait_cpu.py` in the background.
  - **Do non-browser work meanwhile:** drafting, API discovery, guest-API job searches.
- Giant scrolls (`amount: 20000`) on 100-comment threads time out. Scroll in steps of 600–1000.

## Platform specifics
- **Bluesky:** the media button opens a native picker, so paste images from the clipboard. Reply before liking (a like shifts the layout). Reply-gated threads can't be answered, so filter them out first.
- **Instagram:**
  - Comment replies silently fail after a burst, as described under timing in `anti-spam.md`.
  - "Share to Facebook" may be on by default.
  - Instagram defaults to a 1:1 crop; pick 4:5 for carousels.
  - Render slides with `--virtual-time-budget` so web fonts load. Headless Chrome can hang on heavy WebGL pages; the render script kills it after 45 s.
- **Facebook:**
  - Open posts at their URL, not inside the notification modal.
  - Sort comments by "Newest" to find new top-level comments.
  - `js_click` expands "View N replies".
  - Approval groups take hours, so pace them with `pace.py`.
- **X:** intent pages load slowly under load, so wait up to 45 s for the post button. Ctrl+Enter sends; wait for the button to disappear.
- **LinkedIn search:** `sortBy=DD` (date) ignores keywords and returns the same pool of about 100 jobs. Use `sortBy=R` for keyword matches. The guest API needs no login.
- **Contra:** the "Add work" dialog has no reachable file input, so paste the image. Escape leaves a Draft tile behind; delete it through "...".
- **Upwork:** Connects cost money after the free grant, so run Upwork inbound-only (Project Catalog and invites).
- **Reddit r/forhire:** needs account age and karma; don't farm karma.

## Scope and trust
- **Never "help" by editing the owner's repos or sites.** One unrequested branch and page duplicated an existing portfolio page and cost a lot of trust. Read-only; describe changes and let the owner make them.
- **Native file pickers belong to the owner.** If one opens, say so with the exact file and path, and don't touch that page while they use it.
- **Infrastructure detours eat a session.** Chasing a CI token through permission denials and dashboards instead of asking cost hours. Ask in one line first.
