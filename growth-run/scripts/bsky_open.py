#!/usr/bin/env python3
"""List replies on the owner's recent Bluesky threads that the owner has not answered.

Usage: bsky_open.py <owner-handle> [threads_to_scan=70]
Output: time(UTC) handle rkey | text
Open a reply at https://bsky.app/profile/<handle>/post/<rkey>.
Tip (Windows): set PYTHONIOENCODING=utf-8 so emoji print cleanly.
"""
import json
import sys
import urllib.parse
import urllib.request

API = "https://public.api.bsky.app/xrpc/"
if len(sys.argv) < 2:
    sys.exit(__doc__)
OWNER = sys.argv[1]
SCAN = int(sys.argv[2]) if len(sys.argv) > 2 else 70


def g(path):
    return json.load(urllib.request.urlopen(API + path, timeout=20))


feed = g(f"app.bsky.feed.getAuthorFeed?actor={OWNER}&limit=100")["feed"]
uris = [it["post"]["uri"] for it in feed if not it.get("reason")]
out = set()


def walk(node):
    for r in node.get("replies", []) or []:
        p = r.get("post")
        if not p:
            continue
        h = p["author"]["handle"]
        if h != OWNER:
            answered = any(rr.get("post", {}).get("author", {}).get("handle") == OWNER
                           for rr in r.get("replies", []) or [])
            if not answered:
                out.add((p["indexedAt"][:16], h, p["uri"].split("/")[-1],
                         p["record"].get("text", "")[:220].replace("\n", " ")))
        walk(r)


for u in uris[:SCAN]:
    try:
        t = g("app.bsky.feed.getPostThread?depth=6&uri=" + urllib.parse.quote(u, safe=""))["thread"]
    except Exception:
        continue
    walk(t)
for o in sorted(out, reverse=True)[:40]:
    print(o[0], o[1], o[2], "|", o[3])
