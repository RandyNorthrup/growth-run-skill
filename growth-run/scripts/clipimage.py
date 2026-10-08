#!/usr/bin/env python3
"""Put an image on the clipboard silently (paste with Ctrl+V into Bluesky, Contra, etc.).

Usage: clipimage.py <image-path>
Windows: uses Pillow + Win32 API if Pillow is installed; otherwise a hidden PowerShell
(no console window). macOS: osascript. Linux: wl-copy or xclip with the PNG bytes.
"""
import io
import os
import platform
import shutil
import subprocess
import sys

CREATE_NO_WINDOW = 0x08000000


def windows(path):
    try:
        from PIL import Image  # optional dependency
        import ctypes
        from ctypes import wintypes
        img = Image.open(path).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, "BMP")
        dib = buf.getvalue()[14:]  # strip BITMAPFILEHEADER -> CF_DIB
        u32, k32 = ctypes.WinDLL("user32"), ctypes.WinDLL("kernel32")
        k32.GlobalAlloc.restype = wintypes.HGLOBAL
        k32.GlobalLock.restype = wintypes.LPVOID
        k32.GlobalLock.argtypes = [wintypes.HGLOBAL]
        u32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
        h = k32.GlobalAlloc(0x0002, len(dib))
        ctypes.memmove(k32.GlobalLock(h), dib, len(dib))
        k32.GlobalUnlock(h)
        if not u32.OpenClipboard(None):
            raise OSError("clipboard busy")
        u32.EmptyClipboard()
        u32.SetClipboardData(8, h)  # CF_DIB
        u32.CloseClipboard()
        return True
    except ImportError:
        ps = ("Add-Type -AssemblyName System.Windows.Forms,System.Drawing;"
              "[System.Windows.Forms.Clipboard]::SetImage([System.Drawing.Image]::FromFile('%s'))"
              % os.path.abspath(path).replace("'", "''"))
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-STA", "-Command", ps],
                           capture_output=True, creationflags=CREATE_NO_WINDOW)
        return r.returncode == 0


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
