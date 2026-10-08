#!/usr/bin/env python3
"""Recent (under 14h) original posts from chosen Bluesky accounts, ranked by likes + 3*replies.

Usage: bsky_authors.py handle1 handle2 ...
Output: handle rkey | age replies likes | text
"""
import datetime
import json
import sys
import urllib.request

if len(sys.argv) < 2:
    sys.exit(__doc__)
now = datetime.datetime.now(datetime.timezone.utc)
rows = []
for a in sys.argv[1:]:
    try:
        d = json.load(urllib.request.urlopen(
            "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed"
            f"?actor={a}&limit=15&filter=posts_no_replies", timeout=15))
    except Exception as e:
        print("ERR", a, e, file=sys.stderr)
        continue
    for it in d.get("feed", []):
        if it.get("reason"):
            continue
        p = it["post"]
        if p["author"]["handle"] != a:
            continue
        t = datetime.datetime.fromisoformat(p["indexedAt"].replace("Z", "+00:00"))
        age = (now - t).total_seconds() / 3600
        if age > 14:
            continue
        rows.append((p.get("likeCount", 0) + 3 * p.get("replyCount", 0), a, p["uri"].split("/")[-1], age,
                     p.get("replyCount", 0), p.get("likeCount", 0),
                     p["record"].get("text", "")[:150].replace("\n", " ")))
rows.sort(reverse=True)
for s, a, r, age, rc, lc, t in rows[:40]:
    print(f"{a} {r} | {age:.0f}h r{rc} l{lc} | {t}")
