#!/usr/bin/env python3
"""Tally log.tsv (platform<TAB>kind<TAB>target) against per-platform targets.

Usage: tally.py [log.tsv] [x=75,b=75,f=75,i=75]
Platform codes are whatever you log; suggested: x=X, b=Bluesky, f=Facebook, i=Instagram, l=LinkedIn.
Kinds counted toward the target: orig, reply, comment. Others (skip, unfollow, pending) are listed only.
"""
import collections
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "log.tsv"
targets = {}
if len(sys.argv) > 2:
    for part in sys.argv[2].split(","):
        k, v = part.split("=")
        targets[k] = int(v)
COUNTED = {"orig", "reply", "comment"}
counts = collections.defaultdict(collections.Counter)
with open(path, encoding="utf-8") as fh:
    for line in fh:
        if not line.strip() or line.startswith("#"):
            continue
        cols = line.rstrip("\r\n").split("\t")
        if len(cols) < 2:
            continue
        counts[cols[0]][cols[1]] += 1
for plat in sorted(set(counts) | set(targets)):
    c = counts[plat]
    done = sum(v for k, v in c.items() if k in COUNTED)
    tgt = targets.get(plat)
    status = f"{done}/{tgt} ({'DONE' if done >= tgt else f'{tgt - done} to go'})" if tgt else str(done)
    extras = ", ".join(f"{k}={v}" for k, v in sorted(c.items()))
    print(f"{plat}: {status}   [{extras}]")
