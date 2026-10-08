# Staying human: content, timing and platform traps

The fastest way to lose an account, or a group membership, is to look automated. Everything here comes from what platforms and admins actually react to.

## Content

**Don't:**
- **Post the same text everywhere.** Rewrite the idea for each platform: the hook, the length and the ending question. Never paste one post into several groups within the same hour.
- **Write generic praise** ("Great post!", "So true!", "This is amazing"). It's the top bot signal. Every reply must reference something specific in the post.
- **Sound templated.** Vary openings. Don't start five replies with "Love this", "Great point" or "Exactly". Read a batch aloud before posting; if three sound alike, rewrite two.
- **Lean on links.** Organic replies carry none. Original posts carry at most one link, and only when the link is the point. Many groups treat link posts from new members as spam.
- **Over-promote.** Keep self-promotion to about 1 in 4 posts. Strict groups get zero promo: ask a real question and let people find the owner's profile.
- **Use hashtag or emoji walls.** Use one or two tags only where the platform expects them.
- **Hide behind confident vagueness.** A specific, checkable detail (a card's exact effect, a config flag, a version number) reads as human. Get it right: wrong specifics are worse than none, so skip when unsure.
- **Argue with jabs or "are you a bot?" bait.** Don't reply. Flag it to the owner. Never deny being AI and never claim to be human.

**Do:**
- Ask genuine questions. Replies to the owner's own posts are the best engagement there is, so answer every real one.
- Mix in the owner's personal interests now and then, ideally tied back to the niche.
- Match each community's culture. Read a group's top posts before the first post there.

## Timing
- **Spread actions out.** Leave 30–90 seconds between replies, minutes between original posts, and a couple of hours between rounds. Don't empty a platform's quota in one burst; a 75-post target is a day's work, not an hour's.
- **Respect quiet hours** in the owner's time zone. Scheduled Instagram posts cover mornings and evenings; live activity should look like a person's day.
- **Instagram:**
  - Posts: about 2 a day, 8+ hours apart, scheduled ahead.
  - Comment replies: after about 3 in a few minutes, Instagram silently drops them, and Post does nothing. Stop, and come back after about an hour.
- **X:** at most about 12 follows per 15 minutes (the rate-limit toast appears around 14). Keep follows rare anyway.
- **Facebook groups:**
  - Use `pace.py` for every group post. Approval groups need 6+ hours since that group's last post, one per round, and never two approval groups back-to-back (a 3-hour gap).
  - Open groups need about 4 hours.
  - The owner's own group needs about 1 hour.
- **Burst replies under one post** (10+ replies in a row on a busy thread) are fine when people are talking to the owner. Still vary the wording, and keep each reply specific.

## Why admin-approval groups are a trap
- Each post sits in a queue that a few admins work through by hand. Several posts from one person in a short window look like a spam campaign, so admins **decline them, mute the member, or remove them**, and the queue backs up for everyone.
- **Pending posts are invisible.** It's easy to think a post failed and post again; that's a duplicate in the queue. Check the group's "Your pending posts" (or the post's "Your post is pending" banner) before retrying.
- If a previous post is **still pending after a day or more**, set that group to `skip` in `groups.tsv` until it clears. Stacking more posts behind it makes things worse.
- An approved post can go live hours later, so replies arrive late. Keep checking notifications for it later in the day.
- **Rules differ per group.** Some ban links, some ban self-promotion, some want a flair or question format. Record each group's rule in `groups.tsv` (name column) or in the profile.

## Signals to stop and tell the owner
- Any warning toast: "rate limited", "we limit how often…", "your post goes against our standards", "action blocked".
- A post or comment removed by admins, or a "you've been muted" notice.
- Captchas or "confirm it's you" checks. These are the owner's to handle.
- A sudden drop in reach or follows. Slow down for the rest of the day.
