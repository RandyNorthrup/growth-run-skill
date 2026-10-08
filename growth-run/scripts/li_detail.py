#!/usr/bin/env python3
"""Fetch LinkedIn job details through the public guest API (no login).

Usage: li_detail.py <job_id> [job_id ...]
Prints one summary line per job and writes the full descriptions to details.json.
"""
import html
import json
import re
import sys
import time
import urllib.request


def get(jid):
    url = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/" + jid
    page = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                  timeout=20).read().decode("utf8", "replace")
    crit = dict(re.findall(r'description__job-criteria-subheader">\s*(.*?)\s*</h3>\s*<span[^>]*>\s*(.*?)\s*</span>', page, re.S))
    desc = re.search(r"show-more-less-html__markup[^>]*>(.*?)</div>", page, re.S)
    d = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", desc.group(1)))) if desc else ""

    def f(rx):
        x = re.search(rx, page, re.S)
        return html.unescape(x.group(1).strip()) if x else ""
    return dict(id=jid, title=f(r'topcard__title">\s*(.*?)\s*<'), co=f(r"topcard__org-name-link[^>]*>\s*(.*?)\s*<"),
                loc=f(r'topcard__flavor topcard__flavor--bullet">\s*(.*?)\s*<'),
                applicants=f(r"num-applicants__caption[^>]*>\s*(.*?)\s*<"), criteria=crit, description=d)


if len(sys.argv) < 2:
    sys.exit(__doc__)
out = []
for jid in sys.argv[1:]:
    try:
        r = get(jid)
    except Exception as e:
        print(jid, "ERR", e)
        continue
    out.append(r)
    remote = " | remote-in-description" if "remote" in r["description"].lower() else ""
    print(jid, "|", r["title"], "|", r["co"], "|", r["loc"], "|", r["criteria"].get("Employment type", ""), "|",
          r["criteria"].get("Seniority level", ""), "|", r["applicants"] + remote)
    time.sleep(0.7)
with open("details.json", "w", encoding="utf8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
