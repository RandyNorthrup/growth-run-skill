#!/usr/bin/env python3
"""Build an X intent URL. Prints the URL; prints the weighted length to stderr.

Usage: xintent.py <status_id|0> "text"   (0 = new post, otherwise a reply)
Links count as 23 characters; characters above U+2000 count as 2.
"""
import re, sys, urllib.parse

sid, text = sys.argv[1], sys.argv[2]
body = re.sub(r"https?://\S+", "x" * 23, text)
weighted = sum(2 if ord(c) > 0x2000 else 1 for c in body)
print(f"weighted length {weighted}/280", file=sys.stderr)
base = ("https://x.com/intent/post?in_reply_to=%s&text=" % sid) if sid != "0" else "https://x.com/intent/post?text="
print(base + urllib.parse.quote(text, safe=""))
