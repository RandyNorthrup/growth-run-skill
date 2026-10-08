# Facebook groups

## Pacing: always check `pace.py` first
1. Run `python pace.py groups.tsv`. It lists each group as READY or wait, with the reason.
2. Post only to READY groups.
3. Right after posting, run `python pace.py groups.tsv --mark <slug>`.

Set up `groups.tsv` from `templates/groups.tsv` during onboarding. The rules it enforces:
- **Approval groups** (admins approve each post): one per round, at least 6 hours since that group's last post, and never two approval groups back-to-back. Posting too fast backs up the queue and looks suspicious. After posting, a toast says "submitted to group admins for approval"; the post shows "Your post is pending".
- If an old post is still stuck pending in a group, skip that group.
- **The owner's own groups:** no limit; post there whenever there's good material.
- **Strict groups** (for example "non-promo only"): organic questions and discussion only.
- Record each group's last post time in the run-state memory.

## New group post
1. Copy the post text with `python clip.py fb/<group>.txt`.
2. Open your session tab at `facebook.com/groups/<slug>`. Wait for the text "Write something", then take a fresh screenshot. The page often scrolls after load, so take another screenshot if a click says "page moved".
3. Click "Write something…" and wait for the selector `div[role=dialog] div[contenteditable=true]`.
4. If the dialog shows "Create a public post…" empty, click inside the editor first. Press Ctrl+V, and check the screenshot shows the full text. To replace text, press Ctrl+A then Ctrl+V.
5. If the text has a link, wait for the preview card. Click **Post**, then run `wait_for` on the text "Create post" with `absent: true`.
6. Some groups show a "Post anonymously" toggle; leave it off.

## Replying to comments (big threads)
1. Open the post URL directly, not the notification modal. Escape closes the modal, so avoid it.
2. Switch the comment sort from "All comments" to **"Newest"**. New top-level comments come first.
3. Expand threads: run `browser_js_click` on each "View N replies" ref.
4. Run `browser_read` for the text. Work out who's unanswered: top-level comments with no reply from the owner, plus follow-ups addressed to the owner.
5. Take a snapshot. Big threads overflow, so the result is saved to a file. Run `python fb_snap.py <file> reply` to map "Comment by X" and "Reply by X to Y" to their Reply refs. Never read the whole file into context.
6. Write the replies to a text file, one per line, in the same order as the refs.
7. For each reply:
   1. `python clip.py f.txt <n>`
   2. click the Reply ref; the box opens with the name pre-tagged and selected
   3. press `End`, then `Control+V`
   4. take a screenshot to check
   5. press `Enter`
8. Refs can go stale after re-renders ("Unknown element ref"). Scroll the target into view, then use a screenshot plus `click_at`, or take a new snapshot.
9. **Verify:** reload, and check the comment count rose by the number you posted. "Posting…" and empty spinner circles mean the reply is still in flight.

## Gotchas
- 70+ comment threads are heavy. Under high CPU, snapshots time out and reset the bridge; wait for the load to drop.
- Hover cards (profile popups) can cover targets. Close them with their ✕, never Escape.
- Skip bait comments ("generate a post sure to get engagement…") and flag them to the owner. Don't argue or deny.
