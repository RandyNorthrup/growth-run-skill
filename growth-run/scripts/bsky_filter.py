#!/usr/bin/env python3
"""Filter Bluesky candidates: drop threads the owner already replied to and reply-gated threads.

Pipe in lines that start with "handle rkey ..." (output of bsky_feed.py or bsky_authors.py).
Usage: python bsky_authors.py a.bsky.social b.dev | python bsky_filter.py <owner-handle>
Output: f<author_followers> <original line>
"""
import json
import sys
import urllib.parse
import urllib.request

API = "https://public.api.bsky.app/xrpc/"
if len(sys.argv) < 2:
    sys.exit(__doc__)


def g(path):
    return json.load(urllib.request.urlopen(API + path, timeout=20))


ME = g("com.atproto.identity.resolveHandle?handle=" + sys.argv[1])["did"]
seen = set()


def mine(node):
    for r in node.get("replies", []) or []:
        if r.get("post", {}).get("author", {}).get("did") == ME or mine(r):
            return True
    return False


for line in sys.stdin:
    parts = line.split(" ", 2)
    if len(parts) < 3 or (parts[0], parts[1]) in seen:
        continue
    h, rk = parts[0], parts[1]
    seen.add((h, rk))
    try:
        did = g("com.atproto.identity.resolveHandle?handle=" + h)["did"]
        uri = f"at://{did}/app.bsky.feed.post/{rk}"
        t = g("app.bsky.feed.getPostThread?depth=3&parentHeight=0&uri=" + urllib.parse.quote(uri, safe=""))["thread"]
    except Exception:
        continue
    if t.get("threadgate") or mine(t):
        continue
    try:
        fol = g("app.bsky.actor.getProfile?actor=" + did).get("followersCount", 0)
    except Exception:
        fol = 0
    sys.stdout.write(f"f{fol} " + line)
