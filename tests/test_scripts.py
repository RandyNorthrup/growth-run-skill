"""Offline tests for the growth-run helper scripts (no network, no browser, no clipboard).

Run: python -m unittest discover -s tests -v
"""
import datetime as dt
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "growth-run", "scripts")


def run(script, *args, env=None, cwd=None):
    e = dict(os.environ, PYTHONIOENCODING="utf-8", **(env or {}))
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args],
                          capture_output=True, text=True, encoding="utf-8", env=e, cwd=cwd, timeout=60)


class TestCompile(unittest.TestCase):
    def test_all_scripts_compile(self):
        import py_compile
        for name in os.listdir(SCRIPTS):
            if name.endswith(".py"):
                py_compile.compile(os.path.join(SCRIPTS, name), doraise=True)


class TestPace(unittest.TestCase):
    def write(self, rows):
        fd, path = tempfile.mkstemp(suffix=".tsv")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write("# slug\tname\tmode\tmin_hours\tlast_post_utc\n")
            for r in rows:
                fh.write("\t".join(r) + "\n")
        self.addCleanup(os.remove, path)
        return path

    def ago(self, hours):
        return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)).isoformat(timespec="minutes")

    def test_approval_group_waits_six_hours(self):
        p = self.write([["appr", "Approval", "approval", "", self.ago(2)]])
        out = run("pace.py", p).stdout
        self.assertIn("wait", out)

    def test_approval_group_ready_after_window(self):
        p = self.write([["appr", "Approval", "approval", "", self.ago(7)]])
        self.assertIn("READY", run("pace.py", p).stdout)

    def test_no_back_to_back_approval_groups(self):
        p = self.write([["a1", "A1", "approval", "", self.ago(1)],
                        ["a2", "A2", "approval", "", ""]])
        lines = run("pace.py", p).stdout.splitlines()
        a2 = next(l for l in lines if " a2 " in l)
        self.assertTrue(a2.startswith("wait"), a2)
        self.assertIn("another approval group", a2)

    def test_own_group_short_cooldown_and_skip(self):
        p = self.write([["mine", "Mine", "own", "", self.ago(1.5)],
                        ["stuck", "Stuck", "skip", "", ""]])
        lines = run("pace.py", p).stdout.splitlines()
        self.assertTrue(next(l for l in lines if " mine " in l).startswith("READY"))
        self.assertTrue(next(l for l in lines if " stuck " in l).startswith("wait"))

    def test_mark_records_time(self):
        p = self.write([["g", "G", "open", "", ""]])
        self.assertIn("marked g", run("pace.py", p, "--mark", "g").stdout)
        self.assertIn("wait", run("pace.py", p).stdout)


class TestTally(unittest.TestCase):
    def test_counts_and_targets(self):
        with tempfile.TemporaryDirectory() as d:
            log = os.path.join(d, "log.tsv")
            with open(log, "w", encoding="utf-8") as fh:
                fh.write("# header\nx\torig\ta\nx\treply\tb\nx\tskip\tc\nb\treply\td\n")
            out = run("tally.py", log, "x=2,b=3").stdout
            self.assertIn("x: 2/2 (DONE)", out)
            self.assertIn("b: 1/3 (2 to go)", out)


class TestBank(unittest.TestCase):
    def test_check_and_urls(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "bank.tsv"), "w", encoding="utf-8") as fh:
                fh.write("# comment\nshort\tHello world\thttps://example.com\nlong\t" + "x" * 290 + "\t\n")
            out = run("bank.py", "check", cwd=d).stdout
            self.assertRegex(out, r"long\s+x290.*X!")
            self.assertNotIn("X!", [l for l in out.splitlines() if l.startswith("short")][0])
            url = run("bank.py", "b", "short", cwd=d).stdout.strip()
            self.assertTrue(url.startswith("https://bsky.app/intent/compose?text=Hello%20world"))
            self.assertIn("example.com", url)
            self.assertNotIn("example.com", run("bank.py", "x", "short", cwd=d).stdout)


class TestXIntent(unittest.TestCase):
    def test_reply_and_new(self):
        r = run("xintent.py", "123", "hi there https://example.com/x")
        self.assertIn("in_reply_to=123", r.stdout)
        self.assertIn("weighted length 32/280", r.stderr)  # 9 chars + 23 for the link
        self.assertTrue(run("xintent.py", "0", "hi").stdout.startswith("https://x.com/intent/post?text=hi"))


class TestFbSnap(unittest.TestCase):
    def test_maps_reply_refs(self):
        snap = "\n".join([
            '- article "Comment by Ada Lovelace 2 hours ago" [ref=e10]',
            '  - button "Reply" [ref=e11]',
            '  - button "View 2 replies" [ref=e12]',
            '- article "Reply by Alan Turing to Ada Lovelace\'s comment 1 hour ago" [ref=e20]',
            '  - button "Reply" [ref=e21]',
        ])
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
            fh.write(snap)
        self.addCleanup(os.remove, fh.name)
        out = run("fb_snap.py", fh.name).stdout
        self.assertIn("REPLY e11 Comment by Ada Lovelace", out)
        self.assertIn("VIEW  e12 View 2 replies", out)
        self.assertIn("REPLY e21 Reply by Alan Turing", out)


if __name__ == "__main__":
    unittest.main()
