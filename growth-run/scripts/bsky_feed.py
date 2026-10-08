#!/usr/bin/env python3
"""Fresh top-level posts (under 30h) from Bluesky custom feeds, ranked by likes + 3*replies.

Usage: bsky_feed.py at://did:plc:<id>/app.bsky.feed.generator/<name> [...]
Output: handle rkey | age replies likes | text
"""
import datetime
import json
import sys
import urllib.parse
import urllib.request

if len(sys.argv) < 2:
    sys.exit(__doc__)
now = datetime.datetime.now(datetime.timezone.utc)
out = []
for f in sys.argv[1:]:
    try:
        d = json.load(urllib.request.urlopen(
            "https://public.api.bsky.app/xrpc/app.bsky.feed.getFeed?feed=%s&limit=40"
            % urllib.parse.quote(f, safe=":/"), timeout=20))
    except Exception as e:
        print("ERR", f, e, file=sys.stderr)
        continue
    for it in d.get("feed", []):
        p = it["post"]
        r = p["record"]
        if r.get("reply"):
            continue
        t = datetime.datetime.fromisoformat(p["indexedAt"].replace("Z", "+00:00"))
        age = (now - t).total_seconds() / 3600
        if age > 30:
            continue
        out.append((p.get("likeCount", 0) + 3 * p.get("replyCount", 0), age, p["author"]["handle"],
                    p["uri"].split("/")[-1], p.get("replyCount", 0), p.get("likeCount", 0),
                    r.get("text", "")[:160].replace("\n", " ")))
seen = set()
for sc, age, h, rk, rc, lc, txt in sorted(out, reverse=True):
    if rk in seen:
        continue
    seen.add(rk)
    print(f"{h} {rk} | {age:.0f}h r{rc} l{lc} | {txt}")
