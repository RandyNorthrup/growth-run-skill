#!/usr/bin/env python3
"""Render an HTML carousel to PNG slides with headless Chrome (silent, cross-platform).

Each slide is shown at index.html#<n> (see templates/carousel.html).

Usage:
  render_carousel.py --html work/ig/tips/index.html --name tips --count 8 --out ~/Pictures/Instagram
  ... --only 2 3        re-render selected slides
  ... --chrome PATH     Chrome/Chromium binary if not auto-detected
Uses a private profile next to the HTML, so it never touches the owner's Chrome.
"""
import argparse
import os
import platform
import shutil
import subprocess
import time

CANDIDATES = [
    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
]
WINDOWS = platform.system() == "Windows"
NO_WINDOW = 0x08000000 if WINDOWS else 0


def kill_tree(proc):
    if WINDOWS:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, creationflags=NO_WINDOW)
    else:
        proc.kill()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--html", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--count", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", type=int, nargs="*")
    ap.add_argument("--chrome")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--timeout", type=int, default=45)
    a = ap.parse_args()

    chrome = a.chrome or next((p for p in CANDIDATES if p and os.path.exists(p)), None) or shutil.which("chrome")
    if not chrome:
        raise SystemExit("Chrome not found; pass --chrome PATH")
    html = os.path.abspath(a.html)
    src = os.path.dirname(html)
    profile = os.path.join(src, ".render-profile")
    out = os.path.expanduser(a.out)
    os.makedirs(out, exist_ok=True)
    url = "file:///" + html.replace("\\", "/").lstrip("/")
    for i in (a.only or range(1, a.count + 1)):
        png = os.path.join(src, f"{a.name}-{i}.png")
        ok = False
        for _ in range(3):
            if os.path.exists(png):
                os.remove(png)
            cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={profile}",
                   f"--window-size={a.width},{a.height}", "--virtual-time-budget=6000", f"--screenshot={png}", f"{url}#{i}"]
            p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=NO_WINDOW)
            try:
                p.wait(timeout=a.timeout)
            except subprocess.TimeoutExpired:  # hung render (heavy WebGL etc.)
                kill_tree(p)
                time.sleep(2)
            for _ in range(8):
                if os.path.exists(png):
                    break
                time.sleep(0.25)
            if os.path.exists(png):
                ok = True
                break
        if ok:
            shutil.copy2(png, os.path.join(out, f"{a.name}-{i}.png"))
            print(f"ok {a.name}-{i}")
        else:
            print(f"FAILED {a.name}-{i}")


if __name__ == "__main__":
    main()
