# The round loop

## Session start
1. Read the owner profile and run-state memory. Read `rules.md`.
2. If your harness defers tool schemas, load the browser tools first. With chrome-control, these are:
   `browser_snapshot, browser_click, browser_click_at, browser_press_key, browser_wait_for, browser_navigate, browser_read, browser_screenshot, browser_tabs, browser_select_tab, browser_new_tab, browser_close_tab, browser_js_click, browser_scroll, browser_upload`.
   Parameter names that trip people up:
   - `browser_press_key` takes `keys`.
   - `browser_wait_for` takes `timeout_ms` and `absent`.
   - `browser_snapshot` takes no arguments.

   For other browser tools, map the names using the table in `browser-ops.md`.
3. Run `browser_tabs`. Open your own tab with `browser_new_tab`; don't take over the one the owner is viewing.
4. Run `python tally.py log.tsv` to see where each platform stands against its targets.

## Each round
1. **Replies, every platform:**
   - X: the mentions page, then context with `xthread.py`.
   - Bluesky: `bsky_open.py <handle>`.
   - Facebook: the notifications page, then each post sorted "Newest".
   - Instagram: notifications, then the post's comments.

   Draft all the replies for a thread into a text file, one per line. Proofread them as a batch against the rules, then post them line by line with `clip.py`.
2. **Proactive replies on big accounts** in the niche. Good sources are `xsynd.py` and `bsky_authors.py`/`bsky_feed.py | bsky_filter.py`, along with the Instagram posts of niche leaders. These replies count toward the targets and are how new followers find the owner.
3. **Originals:** take the next items from the post bank (`bank.py`), keeping the content mix. Post the same idea on different platforms in different wording; don't cross-post verbatim minute-to-minute.
4. **Instagram:** keep the schedule filled at least 3–4 days ahead.
5. **Facebook groups:** post to each eligible group per the pacing rules. Do the owner's own group whenever there's something good.
6. **Log every action right away** in `log.tsv`. Re-tally after each batch.
7. **Status line** to the owner: what was done and what's next. Keep going.

## Cadence and waiting
- Space the rounds out, roughly every 1–2 hours, so engagement looks human and new replies can accumulate.
- Don't poll in sleep loops. For the next timed round, use a session cron or scheduled wakeup if one is available. Otherwise run a background waiter such as `wait_cpu.py`.
- If the machine is pegged (CPU above 90%) and the browser bridge keeps resetting, stop driving heavy pages. Run `python wait_cpu.py 75` in the background and resume when it returns. See `browser-ops.md`.

## Milestones and memory
After each platform hits its target, and whenever the context is getting long, update `growth-run-state-<slug>.md` with:
- the counts, and what's scheduled with its dates and styles
- the last post time for each Facebook group, which drives the pacing
- open threads to revisit, such as a reply that hit the Instagram throttle
- skips flagged for the owner
- gotchas discovered this session

## End of run
1. Report counts per platform against the targets, skips flagged, any follows with reasons, and open questions.
2. Then, if the profile includes the gig hunt, do the check-in in `jobs.md`.
