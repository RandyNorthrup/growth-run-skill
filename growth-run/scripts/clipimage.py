#!/usr/bin/env python3
"""Put an image on the clipboard silently (paste with Ctrl+V into Bluesky, Contra, etc.).

Usage: clipimage.py <image-path>
Windows: uses Pillow + Win32 API if Pillow is installed; otherwise a hidden PowerShell
(no console window). macOS: osascript. Linux: wl-copy or xclip with the PNG bytes.
"""
import ctypes
import io
import os
import platform
import shutil
import subprocess
import sys

CREATE_NO_WINDOW = 0x08000000
CF_DIB = 8
GMEM_MOVEABLE = 0x0002


def _win32():
    """user32 and kernel32 with prototypes declared.

    Handles are 64-bit on x64 Windows. Without argtypes ctypes passes them as a C int
    and raises "int too long to convert" as soon as a handle value needs more than 32 bits.
    """
    from ctypes import wintypes
    u32 = ctypes.WinDLL("user32", use_last_error=True)
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    u32.OpenClipboard.argtypes = [wintypes.HWND]
    u32.OpenClipboard.restype = wintypes.BOOL
    u32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
    u32.SetClipboardData.restype = wintypes.HANDLE
    k32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
    k32.GlobalAlloc.restype = wintypes.HGLOBAL
    k32.GlobalLock.argtypes = [wintypes.HGLOBAL]
    k32.GlobalLock.restype = wintypes.LPVOID
    k32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
    k32.GlobalFree.argtypes = [wintypes.HGLOBAL]
    k32.GlobalFree.restype = wintypes.HGLOBAL
    return u32, k32


def _global_copy(k32, data):
    """Copy bytes into a moveable global memory block and return its handle."""
    h = k32.GlobalAlloc(GMEM_MOVEABLE, len(data))
    if not h:
        raise OSError("GlobalAlloc failed")
    p = k32.GlobalLock(h)
    if not p:
        k32.GlobalFree(h)
        raise OSError("GlobalLock failed")
    ctypes.memmove(p, data, len(data))
    k32.GlobalUnlock(h)
    return h


def windows(path):
    try:
        from PIL import Image  # optional dependency
    except ImportError:
        ps = ("Add-Type -AssemblyName System.Windows.Forms,System.Drawing;"
              "[System.Windows.Forms.Clipboard]::SetImage([System.Drawing.Image]::FromFile('%s'))"
              % os.path.abspath(path).replace("'", "''"))
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-STA", "-Command", ps],
                           capture_output=True, creationflags=CREATE_NO_WINDOW)
        return r.returncode == 0
    img = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "BMP")
    dib = buf.getvalue()[14:]  # strip BITMAPFILEHEADER -> CF_DIB
    u32, k32 = _win32()
    h = _global_copy(k32, dib)
    if not u32.OpenClipboard(None):
        k32.GlobalFree(h)
        return False  # clipboard busy
    try:
        u32.EmptyClipboard()
        ok = bool(u32.SetClipboardData(CF_DIB, h))  # on success the clipboard owns h
    finally:
        u32.CloseClipboard()
    if not ok:
        k32.GlobalFree(h)
    return ok


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    system = platform.system()
    if system == "Windows":
        ok = windows(path)
    elif system == "Darwin":
        cls = "PNGf" if path.lower().endswith(".png") else "JPEG"
        script = f'set the clipboard to (read (POSIX file "{os.path.abspath(path)}") as «class {cls}»)'
        ok = subprocess.run(["osascript", "-e", script]).returncode == 0
    else:
        data = open(path, "rb").read()
        mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
        cmd = ["wl-copy", "--type", mime] if shutil.which("wl-copy") else ["xclip", "-selection", "clipboard", "-t", mime]
        ok = subprocess.run(cmd, input=data).returncode == 0
    print(("ok image " if ok else "FAILED image ") + path)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
