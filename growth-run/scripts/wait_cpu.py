#!/usr/bin/env python3
"""Block until CPU load stays under a threshold for 3 consecutive checks (silent, no child processes).

Usage: wait_cpu.py [threshold_percent=75] [max_minutes=30] [interval_seconds=10]
Run it in the background; resume heavy browser work when it prints "cpu-ok".
Exit 1 on timeout.
"""
import os
import platform
import sys
import time


def _windows_sampler():
    import ctypes
    from ctypes import wintypes

    k32 = ctypes.WinDLL("kernel32")

    def times():
        idle, kern, user = wintypes.FILETIME(), wintypes.FILETIME(), wintypes.FILETIME()
        k32.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kern), ctypes.byref(user))
        f = lambda t: (t.dwHighDateTime << 32) | t.dwLowDateTime
        return f(idle), f(kern), f(user)  # kernel time includes idle time

    def sample(interval):
        i1, k1, u1 = times()
        time.sleep(interval)
        i2, k2, u2 = times()
        total = (k2 - k1) + (u2 - u1)
        return 100.0 * (1 - (i2 - i1) / total) if total else 0.0
    return sample


def _linux_sampler():
    def read():
        with open("/proc/stat") as fh:
            vals = [int(x) for x in fh.readline().split()[1:]]
        return vals[3] + vals[4], sum(vals)  # idle + iowait, total

    def sample(interval):
        i1, t1 = read()
        time.sleep(interval)
        i2, t2 = read()
        return 100.0 * (1 - (i2 - i1) / (t2 - t1)) if t2 > t1 else 0.0
    return sample


def _loadavg_sampler():
    def sample(interval):
        time.sleep(interval)
        return 100.0 * os.getloadavg()[0] / (os.cpu_count() or 1)
    return sample


def main():
    th = float(sys.argv[1]) if len(sys.argv) > 1 else 75
    max_min = float(sys.argv[2]) if len(sys.argv) > 2 else 30
    interval = float(sys.argv[3]) if len(sys.argv) > 3 else 10
    system = platform.system()
    sample = (_windows_sampler() if system == "Windows"
              else _linux_sampler() if os.path.exists("/proc/stat") else _loadavg_sampler())
    deadline = time.time() + max_min * 60
    ok = 0
    load = 100.0
    while ok < 3:
        load = sample(interval)
        ok = ok + 1 if load < th else 0
        if time.time() > deadline:
            print(f"timeout load={load:.0f}")
            sys.exit(1)
    print(f"cpu-ok {time.strftime('%H:%M:%S')} load={load:.0f}")


if __name__ == "__main__":
    main()
