#!/usr/bin/env python3
"""Setup check for growth-run. Run once per machine: python scripts/doctor.py

Checks Python, Chrome, a silent clipboard round-trip, and that the public APIs are
reachable (Bluesky, X syndication, LinkedIn guest). The gh CLI is optional.
Nothing here posts, logs in or changes settings, and no console windows are opened.
"""
import os
import platform
import shutil
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
results = []


def check(name, ok, detail="", required=True):
    results.append((name, ok, required))
    mark = "OK  " if ok else ("FAIL" if required else "warn")
    print(f"[{mark}] {name}{(' - ' + detail) if detail else ''}")


def reach(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        return urllib.request.urlopen(req, timeout=15).status < 400
    except Exception:
        return False


check("Python 3.8+", sys.version_info >= (3, 8), platform.python_version())

chrome_paths = [
    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
]
chrome = next((p for p in chrome_paths if os.path.exists(p)), None) or shutil.which("google-chrome") or shutil.which("chromium")
check("Google Chrome (owner's browser + carousel rendering)", bool(chrome), chrome or "not found")

try:
    import clip
    probe = "growth-run clipboard probe ✓ “quotes”"
    before = clip.get_clip()
    ok = clip.copy_verified(probe)
    if before:
        clip.set_clip(before)  # restore whatever the owner had copied
    check("Clipboard round-trip (UTF-8, silent)", ok)
except Exception as e:
    check("Clipboard round-trip (UTF-8, silent)", False,
          f"{e} (Linux: install wl-clipboard or xclip)")

check("Bluesky public API", reach("https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor=bsky.app"))
check("X syndication (thread context)", reach("https://cdn.syndication.twimg.com/tweet-result?id=20&token=a"),
      "optional; falls back to the browser", required=False)
check("LinkedIn guest jobs API",
      reach("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=developer"),
      "optional; only for the gig hunt", required=False)
check("gh CLI (read-only README lookups)", bool(shutil.which("gh")), "optional", required=False)

print("""
Browser control is checked by the agent, not this script:
  Proven: chrome-control MCP driving the owner's real, logged-in Chrome.
  Other tools must be able to drive the real logged-in profile (headed), read page text, give element
  refs, click by ref and by coordinates, press keys, take screenshots, upload to a file input,
  and paste from the system clipboard. See reference/browser-ops.md.
""")
failed = [n for n, ok, req in results if req and not ok]
print("READY" if not failed else "Fix required items: " + "; ".join(failed))
sys.exit(1 if failed else 0)
