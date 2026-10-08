#!/usr/bin/env python3
"""Search LinkedIn jobs through the public guest API (no login).

Usage: li_search.py "<keywords>" ["extra=query&params"]
Defaults: remote (f_WT=2), Easy Apply (f_AL=true), posted in the last 7 days (f_TPR=r604800).
Extra params are appended and override nothing already set, e.g.:
  "f_JT=C&sortBy=R"          contract only, relevance sort (respects keywords)
  "f_TPR=r86400"             last 24 hours (use instead of the default window)
Location: set LI_LOCATION (default "United States") and LI_GEOID (default 103644278).
Output: job_id | title | company | location | posted | salary
Then: li_detail.py <job_id> ...
"""
import html
import os
import re
import sys
import time
import urllib.parse
import urllib.request

if len(sys.argv) < 2:
    sys.exit(__doc__)
kw = sys.argv[1]
extra = sys.argv[2] if len(sys.argv) > 2 else ""
base = {"keywords": kw, "location": os.environ.get("LI_LOCATION", "United States"),
        "geoId": os.environ.get("LI_GEOID", "103644278"), "f_WT": "2", "f_AL": "true"}
if "f_TPR=" not in extra:
    base["f_TPR"] = "r604800"
seen = set()
for start in (0, 25, 50):
    q = urllib.parse.urlencode({**base, "start": start}) + ("&" + extra if extra else "")
    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?" + q
    try:
        page = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                      timeout=20).read().decode("utf8", "replace")
    except Exception as e:
        print("ERR", e, file=sys.stderr)
        break
    n = 0
    for card in page.split("<li"):
        m = re.search(r"jobPosting:(\d+)", card)
        if not m or m.group(1) in seen:
            continue
        seen.add(m.group(1))
        n += 1

        def f(rx):
            x = re.search(rx, card, re.S)
            return html.unescape(x.group(1).strip()) if x else ""
        print(m.group(1), "|", f(r'base-search-card__title">\s*(.*?)\s*<'), "|",
              f(r'base-search-card__subtitle">.*?>\s*(.*?)\s*<'), "|",
              f(r'job-search-card__location">\s*(.*?)\s*<'), "|", f(r'datetime="(.*?)"'), "|",
              f(r'job-search-card__salary-info">\s*(.*?)\s*<'))
    if n == 0:
        break
    time.sleep(1)
