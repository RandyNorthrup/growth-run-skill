#!/usr/bin/env python3
"""Facebook group pacing guard. Enforces the anti-spam rules mechanically.

groups.tsv columns (tab-separated, # comments allowed):
  slug  name  mode  min_hours  last_post_utc
mode:
  approval  admins approve each post -> at most one approval group per round,
            min_hours since that group's last post (default 6), and never two
            approval-group posts within APPROVAL_GAP_HOURS of each other
  open      posts go live -> min_hours since last post (default 4)
  own       the owner's group -> min_hours (default 1)
  strict    like open, but organic/non-promo posts only
  skip      never post (e.g. an old post is stuck pending)

Usage:
  pace.py groups.tsv                 list groups and whether each is eligible now
  pace.py groups.tsv --mark <slug>   record a post to <slug> at the current time
"""
import datetime as dt
import sys

APPROVAL_GAP_HOURS = 3.0
DEFAULTS = {"approval": 6.0, "open": 4.0, "own": 1.0, "strict": 4.0, "skip": 1e9}


def load(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip() or line.startswith("#"):
                rows.append(("comment", line.rstrip("\r\n")))
                continue
            c = (line.rstrip("\r\n").split("\t") + ["", "", "", "", ""])[:5]
            rows.append(("row", c))
    return rows


def parse(ts):
    return dt.datetime.fromisoformat(ts) if ts else None


def save(path, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for kind, r in rows:
            fh.write((r if kind == "comment" else "\t".join(r)) + "\n")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    rows = load(path)
    now = dt.datetime.now(dt.timezone.utc)
    if len(sys.argv) > 3 and sys.argv[2] == "--mark":
        for kind, r in rows:
            if kind == "row" and r[0] == sys.argv[3]:
                r[4] = now.isoformat(timespec="minutes")
                save(path, rows)
                print("marked", r[0], r[4])
                return
        sys.exit("slug not found: " + sys.argv[3])
    data = [r for kind, r in rows if kind == "row"]
    approval_times = [parse(r[4]) for r in data if r[2] == "approval" and r[4]]
    last_approval = max(approval_times) if approval_times else None
    for slug, name, mode, min_h, last in data:
        mode = mode or "open"
        need = float(min_h) if min_h else DEFAULTS.get(mode, 4.0)
        last_t = parse(last)
        since = (now - last_t).total_seconds() / 3600 if last_t else None
        ok = mode != "skip" and (since is None or since >= need)
        why = "" if since is None else f"{since:.1f}h since last"
        if ok and mode == "approval" and last_approval:
            gap = (now - last_approval).total_seconds() / 3600
            if gap < APPROVAL_GAP_HOURS:
                ok = False
                why += f"; another approval group posted {gap:.1f}h ago"
        state = "READY" if ok else "wait "
        print(f"{state} {mode:8} {slug:28} need {need:g}h  {why}  {name}")


if __name__ == "__main__":
    main()
