#!/usr/bin/env python3
"""Silent, cross-platform clipboard copy with verification (no console windows).

Usage:
  clip.py FILE        copy the whole file (multi-line post)
  clip.py FILE N      copy line N (1-based)
  clip.py --text "s"  copy a literal string
Windows: Win32 clipboard API via ctypes (no PowerShell, nothing pops up).
macOS: pbcopy/pbpaste. Linux: wl-copy/wl-paste or xclip.
Prints "ok=True :: <text>" when the clipboard verifiably holds the text.
"""
import platform
import shutil
import subprocess
import sys
import time

WINDOWS = platform.system() == "Windows"

if WINDOWS:
    import ctypes
    from ctypes import wintypes

    CF_UNICODETEXT = 13
    GMEM_MOVEABLE = 0x0002
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    user32.OpenClipboard.argtypes = [wintypes.HWND]
    user32.OpenClipboard.restype = wintypes.BOOL
    user32.CloseClipboard.restype = wintypes.BOOL
    user32.EmptyClipboard.restype = wintypes.BOOL
    user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
    user32.SetClipboardData.restype = wintypes.HANDLE
    user32.GetClipboardData.argtypes = [wintypes.UINT]
    user32.GetClipboardData.restype = wintypes.HANDLE
    kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
    kernel32.GlobalAlloc.restype = wintypes.HGLOBAL
    kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalLock.restype = wintypes.LPVOID
    kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]

    def _open():
        for _ in range(20):  # another app may hold the clipboard briefly
            if user32.OpenClipboard(None):
                return True
            time.sleep(0.05)
        return False

    def set_clip(text):
        data = text.encode("utf-16-le") + b"\x00\x00"
        if not _open():
            return
        try:
            user32.EmptyClipboard()
            h = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(data))
            p = kernel32.GlobalLock(h)
            ctypes.memmove(p, data, len(data))
            kernel32.GlobalUnlock(h)
            user32.SetClipboardData(CF_UNICODETEXT, h)  # clipboard now owns h
        finally:
            user32.CloseClipboard()

    def get_clip():
        if not _open():
            return ""
        try:
            h = user32.GetClipboardData(CF_UNICODETEXT)
            if not h:
                return ""
            p = kernel32.GlobalLock(h)
            try:
                return ctypes.wstring_at(p)
            finally:
                kernel32.GlobalUnlock(h)
        finally:
            user32.CloseClipboard()
else:
    def _run(cmd, data=None):
        return subprocess.run(cmd, input=data, capture_output=True)

    def set_clip(text):
        b = text.encode("utf-8")
        if platform.system() == "Darwin":
            _run(["pbcopy"], b)
        elif shutil.which("wl-copy"):
            _run(["wl-copy"], b)
        else:
            _run(["xclip", "-selection", "clipboard"], b)

    def get_clip():
        if platform.system() == "Darwin":
            r = _run(["pbpaste"])
        elif shutil.which("wl-paste"):
            r = _run(["wl-paste", "--no-newline"])
        else:
            r = _run(["xclip", "-selection", "clipboard", "-o"])
        return r.stdout.decode("utf-8", "replace")


def copy_verified(text):
    for _ in range(10):
        set_clip(text)
        time.sleep(0.1)
        if get_clip().replace("\r", "").rstrip() == text.replace("\r", "").rstrip():
            return True
        time.sleep(0.2)
    return False


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--text":
        text = sys.argv[2]
    else:
        with open(sys.argv[1], encoding="utf-8") as fh:
            text = fh.read()
        if len(sys.argv) > 2:
            text = text.splitlines()[int(sys.argv[2]) - 1]
    text = text.rstrip()
    ok = copy_verified(text)
    # ASCII-safe echo so Windows consoles never choke on emoji
    print(f"ok={ok} :: {text[:120]}".encode("ascii", "replace").decode())
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
