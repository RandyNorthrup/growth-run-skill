#!/usr/bin/env python3
"""Show an X post's author, text and what it replies to, using the public syndication endpoint.

Usage: xthread.py <status_id> [status_id ...]
"""
import json, sys, urllib.request


def get(i):
    req = urllib.request.Request(
        f"https://cdn.syndication.twimg.com/tweet-result?id={i}&token=a",
        headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=20))


for i in sys.argv[1:]:
    try:
        d = get(i)
    except Exception as e:
        print(i, "ERR", e)
        continue
    user = d.get("user", {}).get("screen_name", "?")
    print(f"== {i} @{user}: {d.get('text', '')}")
    parent = d.get("parent")
    if parent:
        print(f"   in reply to @{parent.get('user', {}).get('screen_name', '?')}: {parent.get('text', '')}")
    elif d.get("in_reply_to_screen_name"):
        print(f"   in reply to @{d['in_reply_to_screen_name']} ({d.get('in_reply_to_status_id_str')})")
