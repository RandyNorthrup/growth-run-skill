# Bluesky

## Discovery via the public API (no login, no browser)
- **Unanswered replies to the owner:** `PYTHONIOENCODING=utf-8 python bsky_open.py <owner-handle>`. It walks the owner's recent threads and lists replies with no reply from the owner.
- **Thread context:**
  1. Resolve the handle: `com.atproto.identity.resolveHandle?handle=<h>` gives the DID.
  2. Build `at://<did>/app.bsky.feed.post/<rkey>`.
  3. Fetch `app.bsky.feed.getPostThread?parentHeight=3&uri=<at-uri>` and read the parent chain, to see who is actually talking to whom.
- **Fresh posts to engage with:**
  - `bsky_authors.py <handles…>` for niche leaders' recent originals.
  - `bsky_feed.py <feed-uri…>` for custom feeds.
  - Pipe either into `bsky_filter.py <owner-handle>`. It drops threads already replied to and reply-gated threads, and adds follower counts.
- **Follower check before a rare follow:** `app.bsky.actor.getProfile?actor=<h>` returns `followersCount`.
- All endpoints live under `https://public.api.bsky.app/xrpc/`.

## Reply flow (browser)
1. Draft the replies in a TSV, one per line: `handle/post/rkey<TAB>text`. Copy each with `python clip.py <file> <n>`; keep a plain text file of the replies in the same order.
2. Navigate to `https://bsky.app/profile/<handle>/post/<rkey>`.
3. Click the **"Write your reply"** bar under the post, using a fresh screenshot plus `click_at`. Wait for the selector `.ProseMirror`, click inside it, then press Ctrl+V.
4. Press Ctrl+Enter, then run `wait_for` on `.ProseMirror` with `absent: true`.
5. Reply before liking; liking shifts the layout.

## New posts
- `https://bsky.app/intent/compose?text=<urlencoded>` (300 characters), or `python bank.py b <key>`.
- **Images:** there is no file input, and the media button opens a native picker, so avoid it. Instead, put the image on the clipboard (`python clipimage.py <img>`) and press Ctrl+V in the composer. "+ALT" adds alt text. The "+" next to the language selector adds a thread post.
- The snapshot often truncates before the composer modal, so use screenshots and `click_at`. Screenshot coordinates can be scaled; if small targets miss, multiply by the reported ratio.
- **Link card:** the first link becomes the card. Make sure it's the owner's link, not an accidental autolinked word.
