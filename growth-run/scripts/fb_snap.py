#!/usr/bin/env python3
"""Map Facebook comment authors to their Reply and "View N replies" refs from a saved snapshot.

When a browser snapshot is too big, the harness saves it to a file. Parse that file
instead of reading it into context.

Usage: fb_snap.py <snapshot-file> [all|reply|view]
Output:
  REPLY e140 Reply by Jordan Price to Sean Wendland's comment 3 hours ago
  VIEW  e241 View 2 replies
Refs go stale after the page re-renders; re-snapshot if a click says "Unknown element ref".
"""
import json
import re
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)
mode = sys.argv[2] if len(sys.argv) > 2 else "all"
raw = open(sys.argv[1], encoding="utf-8").read()
try:  # some harnesses save [{"type":"text","text":"..."}]
    text = json.loads(raw)[0]["text"]
except Exception:
    text = raw

current = None
for line in text.splitlines():
    m = re.search(r'article "((?:Comment|Reply) by [^"]+)" \[ref=(e\d+)\]', line)
    if m:
        current = m.group(1)
    if mode in ("all", "view"):
        v = re.search(r'button "((?:View|See) [^"]*repl[^"]*|View more comments|View previous comments)" \[ref=(e\d+)\]', line)
        if v:
            print("VIEW ", v.group(2), v.group(1))
    if mode in ("all", "reply"):
        r = re.search(r'button "Reply" \[ref=(e\d+)\]', line)
        if r and current:
            print("REPLY", r.group(1), current)
            current = None
