#!/usr/bin/env python3
"""Self-check for pipeline.py. Run: python3 test_pipeline.py — asserts, no framework."""
import json
import os
import tempfile

import pipeline


def run(*argv):
    """Invoke a command, capture the JSON it prints."""
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        pipeline.main(list(argv))
    return json.loads(buf.getvalue())


def write_leads(path, leads):
    with open(path, "w") as f:
        json.dump(leads, f)


def main():
    with tempfile.TemporaryDirectory() as d:
        leads = os.path.join(d, "leads.json")
        write_leads(leads, [
            {"profile_url": "u/a", "name": "Ann", "bucket": "warm", "context_note": "x"},
            {"profile_url": "u/b", "name": "Bo", "bucket": "warm"},
            {"profile_url": "u/a", "name": "Ann dup", "bucket": "warm"},  # dupe
        ])
        r = run("add-leads", "--data-dir", d, "--file", leads)
        assert r == {"added": 2, "skipped": 1, "total": 2}, r

        # re-adding same file adds nothing
        r = run("add-leads", "--data-dir", d, "--file", leads)
        assert r["added"] == 0 and r["total"] == 2, r

        # both new leads are due (no next_due_date yet)
        r = run("due", "--data-dir", d, "--today", "2026-07-01", "--intervals", "0,4,7", "--max-steps", "3")
        assert r["count"] == 2, r
        assert {x["profile_url"] for x in r["due"]} == {"u/a", "u/b"}, r
        assert all(x["next_step"] == 1 for x in r["due"]), r

        # daily cap trims
        r = run("due", "--data-dir", d, "--today", "2026-07-01", "--daily-cap", "1")
        assert r["count"] == 1, r

        # send step 1 to Ann on 07-01 -> step 1, active, next_due = +4 (intervals[1])
        r = run("mark-sent", "--data-dir", d, "--url", "u/a", "--date", "2026-07-01",
                "--intervals", "0,4,7", "--max-steps", "3")
        assert r == {"profile_url": "u/a", "step": 1, "status": "active",
                     "next_due_date": "2026-07-05"}, r

        # Ann not due same day; Bo still due
        r = run("due", "--data-dir", d, "--today", "2026-07-01")
        assert {x["profile_url"] for x in r["due"]} == {"u/b"}, r
        # Ann due on 07-05
        r = run("due", "--data-dir", d, "--today", "2026-07-05")
        assert "u/a" in {x["profile_url"] for x in r["due"]}, r

        # Ann replies -> terminal, never due again
        r = run("mark-replied", "--data-dir", d, "--url", "u/a", "--today", "2026-07-02")
        assert r == {"profile_url": "u/a", "status": "replied"}, r
        r = run("due", "--data-dir", d, "--today", "2026-08-01")
        assert "u/a" not in {x["profile_url"] for x in r["due"]}, r

        # walk Bo to done (step 3 == max_steps)
        run("mark-sent", "--data-dir", d, "--url", "u/b", "--date", "2026-07-01")  # step1 -> next 07-05
        run("mark-sent", "--data-dir", d, "--url", "u/b", "--date", "2026-07-05")  # step2 -> +7 = 07-12
        r = run("mark-sent", "--data-dir", d, "--url", "u/b", "--date", "2026-07-12")  # step3 -> done
        assert r["step"] == 3 and r["status"] == "done" and r["next_due_date"] == "", r
        r = run("due", "--data-dir", d, "--today", "2027-01-01")
        assert r["count"] == 0, r  # nobody left to message

        r = run("status", "--data-dir", d)
        assert r == {"total": 2, "by_status": {"replied": 1, "done": 1},
                     "by_bucket": {"warm": 2}}, r

    print("ok")


if __name__ == "__main__":
    main()
