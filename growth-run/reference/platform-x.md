# X (Twitter)

## Replies and posts via intent URLs (most reliable)
1. Build the URL: `python xintent.py <status_id> "reply text"`. Use `0` as the id for a new post. It prints the URL and, on stderr, the length (links count as 23).
2. Run `browser_navigate` to that URL.
3. Run `browser_wait_for` with selector `[data-testid=tweetButton]` and `timeout_ms` 45000. The page loads slowly when the CPU is busy.
4. Run `browser_press_key` with `keys` set to `Control+Enter`.
5. Run `browser_wait_for` on the same selector with `absent: true`. When the composer closes, the post went out.
6. Spot-check on the owner's profile every few posts.

## Context before replying
- `python xthread.py <id>` uses the public syndication endpoint `cdn.syndication.twimg.com/tweet-result?id=<id>&token=a` to get the text, author and parent. Read what's being replied to; never reply blind.
- **Finding the owner's mentions:** navigate to `x.com/notifications/mentions` and run `browser_read`. Compare against `log.tsv` to see what's already answered.
- **Finding big-account posts to reply to:** `python xsynd.py 12 handle1 handle2 …` lists recent originals with likes, replies and follower counts.

## Images and threads
- Open `x.com/compose/post`. The page holds two composers; the hidden file input in the snapshot belongs to the timeline one behind the modal.
- Call `browser_upload` on the modal's **"Add photos or video" button ref**.
- "Add description" adds alt text. The "+" builds a thread; then click the **"Post all"** ref. Ctrl+Enter can open "Save post?".

## Limits and gotchas
- Follows: at most about 12 per 15 minutes; the toast "you are rate limited" appears around 14.
- Premium raises the post length limit, but keep posts under 280 weighted characters for reach and cross-posting. Characters above U+2000 count as 2.
- The bridge tends to drop roughly every 20 X actions. See `browser-ops.md` for recovery.
- Words ending in a real TLD autolink. Reword file names ("the agents file").
