#!/usr/bin/env python3
"""Wait for a fresh chrome-control native host after a bridge drop (Windows; silent).

The Chrome extension respawns `chrome_control_mcp.exe` with a command line that contains
"chrome-extension://". When a new one appears, call browser_tabs again.

Usage: bridge_wait.py [max_minutes=5]
       bridge_wait.py --list        show native hosts (Chrome-spawned vs session servers)
Only for chrome-control; other browser tools have their own reconnect behavior.
"""
import json
import subprocess
import sys
import time

CREATE_NO_WINDOW = 0x08000000
PS = ("Get-CimInstance Win32_Process -Filter \"Name='chrome_control_mcp.exe'\" | "
      "Select-Object ProcessId,@{n='Created';e={$_.CreationDate.ToUniversalTime().ToString('o')}},"
      "@{n='Chrome';e={$_.CommandLine -like '*chrome-extension://*'}} | ConvertTo-Json -Compress")


def hosts():
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", PS],
                       capture_output=True, text=True, creationflags=CREATE_NO_WINDOW, timeout=60)
    out = r.stdout.strip()
    if not out:
        return []
    data = json.loads(out)
    return data if isinstance(data, list) else [data]


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        for h in hosts():
            print(h["ProcessId"], h["Created"], "chrome-spawned" if h["Chrome"] else "session-server")
        return
    max_min = float(sys.argv[1]) if len(sys.argv) > 1 else 5
    start = {h["ProcessId"] for h in hosts() if h["Chrome"]}
    deadline = time.time() + max_min * 60
    while time.time() < deadline:
        now = {h["ProcessId"] for h in hosts() if h["Chrome"]}
        new = now - start
        if new:
            time.sleep(15)  # let the extension attach before calling browser_tabs
            print("host-up", sorted(new))
            return
        if not now:
            start = set()  # all hosts gone; the next one to appear is fresh
        time.sleep(3)
    print("timeout: no new host; ask the owner to reload the extension or close a stuck tab")
    sys.exit(1)


if __name__ == "__main__":
    main()
