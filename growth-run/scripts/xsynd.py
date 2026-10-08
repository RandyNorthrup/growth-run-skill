#!/usr/bin/env python3
"""Recent original posts from X accounts, using the public syndication timeline.

Usage: xsynd.py <max_age_hours> handle1 handle2 ...
Output: handle id | age fav replies followers | text
The endpoint is unofficial and can change; if it errors, fall back to reading
the account's profile page in the browser.
"""
import datetime
import json
import re
import sys
import urllib.request

if len(sys.argv) < 3:
    sys.exit(__doc__)
hours = float(sys.argv[1])
now = datetime.datetime.now(datetime.timezone.utc)
rows = []
for name in sys.argv[2:]:
    try:
        req = urllib.request.Request(
            "https://syndication.twitter.com/srv/timeline-profile/screen-name/" + name,
            headers={"User-Agent": "Mozilla/5.0"})
        page = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', page, re.S)
        entries = json.loads(m.group(1))["props"]["pageProps"]["timeline"]["entries"]
    except Exception as e:  # network, rate limit or format change
        print("ERR", name, e, file=sys.stderr)
        continue
    for e in entries:
        t = e.get("content", {}).get("tweet")
        if not t or t.get("in_reply_to_status_id_str") or t.get("retweeted_status"):
            continue
        if t["user"]["screen_name"].lower() != name.lower():
            continue
        ts = datetime.datetime.strptime(t["created_at"], "%a %b %d %H:%M:%S %z %Y")
        age = (now - ts).total_seconds() / 3600
        if age > hours:
            continue
        txt = (t.get("full_text") or t.get("text") or "").replace("\n", " ")
        rows.append((t.get("favorite_count", 0), name, t["id_str"], age, t.get("reply_count", 0),
                     t["user"].get("followers_count", 0), txt[:220]))
rows.sort(reverse=True)
for fav, name, i, age, rc, fol, txt in rows:
    print(f"{name} {i} | {age:.1f}h fav{fav} r{rc} f{fol} | {txt}")
