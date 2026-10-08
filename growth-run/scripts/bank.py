#!/usr/bin/env python3
"""Post bank helper. bank.tsv lines: key<TAB>text<TAB>optional link   (# lines are comments)

Usage (reads $BANK or ./bank.tsv):
  bank.py check          flag posts too long for X (280 weighted) or Bluesky (300)
  bank.py x <key>        X intent URL (link left out; put links in a reply)
  bank.py b <key>        Bluesky compose intent URL (link appended)
  bank.py text <key> [+] raw text; add any 3rd argument to append the link
"""
import os
import sys
import urllib.parse

path = os.environ.get("BANK", "bank.tsv")
rows = {}
with open(path, encoding="utf-8") as fh:
    for line in fh:
        line = line.rstrip("\r\n")
        if not line or line.startswith("#"):
            continue
        p = (line.split("\t") + ["", ""])[:3]
        rows[p[0]] = (p[1], p[2])


def xw(t):
    return sum(2 if ord(c) > 0x2000 else 1 for c in t)


cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
if cmd == "check":
    for k, (t, link) in rows.items():
        b = len(t) + (len(link) + 2 if link else 0)
        flag = ("X! " if xw(t) > 280 else "") + ("B!" if b > 300 else "")
        print(f"{k:14} x{xw(t):3} b{b:3} {flag}")
elif cmd == "x":
    t, _ = rows[sys.argv[2]]
    print("https://x.com/intent/post?text=" + urllib.parse.quote(t, safe=""))
elif cmd == "b":
    t, link = rows[sys.argv[2]]
    print("https://bsky.app/intent/compose?text=" + urllib.parse.quote(t + ("\n\n" + link if link else ""), safe=""))
elif cmd == "text":
    t, link = rows[sys.argv[2]]
    print(t + ("\n\n" + link if link and len(sys.argv) > 3 else ""))
else:
    sys.exit(__doc__)
