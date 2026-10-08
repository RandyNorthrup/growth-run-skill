# Browser operations

## Which browser tool?
**Proven:** the chrome-control MCP, driving the owner's real, logged-in Chrome. Every flow in this skill was run with it, and the tool names below are its names.

**Other tools should work** if they can do all of the following. They are untested, so do a dry run on each platform first.

| Capability needed | chrome-control | Playwright MCP | Claude in Chrome extension |
|---|---|---|---|
| Drive the owner's real logged-in profile | yes (extension) | extension/bridge mode or a persistent profile | yes (runs inside Chrome) |
| Navigate / open own tab | `browser_navigate`, `browser_new_tab` | `browser_navigate`, `browser_tabs` | navigate, tabs |
| Page text | `browser_read` | `browser_snapshot` | read page / get text |
| Element refs + click by ref | `browser_snapshot`, `browser_click` | `browser_snapshot`, `browser_click` | find + click |
| Click by coordinates | `browser_click_at` | `browser_mouse_click_xy` (vision mode) | computer click |
| Keys (Ctrl+V, Ctrl+Enter, End) | `browser_press_key` | `browser_press_key` | key |
| Screenshot | `browser_screenshot` | `browser_take_screenshot` | screenshot |
| Upload to a hidden file input | `browser_upload` | `browser_file_upload` | form input (varies) |
| Wait for text/selector/absence | `browser_wait_for` | `browser_wait_for` | poll with read |

Hard requirements whatever the tool:
- **The real profile.** A fresh automation profile isn't logged in, and repeated logins from a "new device" trigger checks.
- **The system clipboard.** Every reply is pasted, because typing character by character is slow and trips bot detection.
- **A headed browser.** Platforms treat headless sessions as bots.

Sessions from other agents (Codex, Gemini CLI and so on) can use any of these through their MCP configuration. Map the tool names using the table and keep the flows the same.

## Tabs
- `browser_tabs` lists every tab. "active" means the tab the **owner** is looking at, not the one you are driving.
- **Your session tab:**
  - `browser_new_tab <url>` opens it in the background, in the AI CONTROL group.
  - `browser_select_tab <index>` re-selects it. Call `browser_tabs` immediately before, because the index must match.
- Never navigate, close or type in the owner's tabs.
- `browser_close_tab` with no index closes the session tab.

## Reading pages
- `browser_read` returns the page text. It's cheap; prefer it for "what's on this page".
- `browser_snapshot` gives the interactive tree with refs. On heavy pages it overflows and is **saved to a file**. Parse that file with a script such as `fb_snap.py`; never read it whole into context.
- `browser_screenshot` before every `browser_click_at`. A click is refused with "page moved" if the page scrolled since the last screenshot.
- `browser_js_click <ref>` is for elements that ignore pointer clicks, such as "View N replies".
- `browser_scroll` with a `ref` scrolls the container holding that element, such as a comment pane. Without one, it scrolls the page under the viewport center.

## Clipboard (Windows)
- Use `python clip.py <file> [line]`. It calls the Win32 clipboard API directly (no PowerShell, no console window), verifies with retries and prints `ok=True`. PowerShell `Set-Clipboard` sometimes leaves the clipboard empty and flashes a window, so don't use it.
- Images: `python clipimage.py <image>`, which is silent.
- Paste with `browser_press_key` `Control+V` after focusing the editor. Check the focus field in the result: `div` or `textarea` means it's in the editor, `body` means focus was lost.

## Bridge drops and recovery
**Symptoms:**
- "browser did not reply within 30000 ms (connection reset)"
- "Chrome Control MCP browser-control extension is not attached"

**Recovery:**
1. Wait for a fresh Chrome-spawned native host: run `python bridge_wait.py` (silent, no console window). It watches for a new `chrome_control_mcp.exe` whose command line contains `chrome-extension://`, then waits 15 s for the extension to attach. `python bridge_wait.py --list` shows Chrome-spawned hosts and session servers.
2. Call `browser_tabs`.
3. If a tab reports "DevTools (or another debugger) is attached", close that tab and open a fresh one.
4. **Reconnect loop**, where every reconnect latches onto the same hung tab: stop the stale Chrome-spawned host (never the hosts without `chrome-extension://`, which belong to other sessions). The extension respawns one within about a minute. If the hung tab can't be closed through the bridge, ask the owner to close it.

**Avoid:**
- chaining snapshot or read straight after navigating to a heavy single-page app; wait or screenshot first
- giant `browser_scroll` amounts on heavy pages

## CPU load
- If other work on the machine pegs the CPU (above 90%), heavy pages such as big Facebook threads time out and reset the bridge.
- Check with `(Get-CimInstance Win32_Processor | Measure-Object LoadPercentage -Average).Average`.
- Don't kill the owner's processes. Run `python wait_cpu.py 75` in the background, do non-browser work meanwhile (drafting, API discovery, job searches through the guest API), and resume when it returns.

## Native dialogs
- Never click buttons that open OS file pickers. Use `browser_upload` on the hidden filechooser ref, or paste through the clipboard.
- If a dialog opens anyway, tell the owner the exact file name and full path, and leave that page alone until they say done.
