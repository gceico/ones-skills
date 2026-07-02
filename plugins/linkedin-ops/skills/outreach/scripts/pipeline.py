#!/usr/bin/env python3
"""outreach.csv state engine for linkedin-ops.

Owns all bookkeeping so the skill spends tokens on the browser + messages, not on
parsing CSVs. stdlib only. Every command prints JSON to stdout.

Commands:
  add-leads   --data-dir D --file leads.json
  due         --data-dir D --today YYYY-MM-DD [--max-steps 3] [--intervals 0,4,7] [--daily-cap 15]
  mark-sent   --data-dir D --url U --date YYYY-MM-DD [--max-steps 3] [--intervals 0,4,7]
  mark-replied --data-dir D --url U
  status      --data-dir D

outreach.csv de-dupe key: profile_url. status in new/active/replied/done/stopped.
replied + stopped + done are terminal (never re-queued).
"""
import argparse
import csv
import datetime
import json
import os
import sys

HEADER = [
    "profile_url", "name", "headline", "source", "bucket", "icp_score",
    "context_note", "status", "step", "last_sent_date", "next_due_date",
    "last_checked_date", "notes",
]
TERMINAL = {"replied", "done", "stopped"}


def _path(data_dir):
    return os.path.join(data_dir, "outreach.csv")


def _read(data_dir):
    p = _path(data_dir)
    if not os.path.exists(p):
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write(data_dir, rows):
    os.makedirs(data_dir, exist_ok=True)
    with open(_path(data_dir), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in HEADER})


def _parse_intervals(s):
    return [int(x) for x in str(s).split(",") if x.strip() != ""]


def _add_days(date_str, n):
    d = datetime.date.fromisoformat(date_str)
    return (d + datetime.timedelta(days=n)).isoformat()


def cmd_add_leads(a):
    rows = _read(a.data_dir)
    seen = {r["profile_url"] for r in rows}
    with open(a.file, encoding="utf-8") as f:
        incoming = json.load(f)
    added = skipped = 0
    for lead in incoming:
        url = (lead.get("profile_url") or "").strip()
        if not url or url in seen:
            skipped += 1
            continue
        seen.add(url)
        row = {k: "" for k in HEADER}
        row.update({k: lead.get(k, "") for k in HEADER if k in lead})
        row["profile_url"] = url
        row["status"] = "new"
        row["step"] = "0"
        rows.append(row)
        added += 1
    _write(a.data_dir, rows)
    print(json.dumps({"added": added, "skipped": skipped, "total": len(rows)}))


def cmd_due(a):
    rows = _read(a.data_dir)
    today = a.today
    out = []
    for r in rows:
        if r["status"] in TERMINAL:
            continue
        if r["status"] not in ("new", "active"):
            continue
        if int(r.get("step") or 0) >= a.max_steps:
            continue
        nd = r.get("next_due_date") or ""
        if nd and nd > today:
            continue
        out.append({
            "profile_url": r["profile_url"], "name": r.get("name", ""),
            "headline": r.get("headline", ""), "bucket": r.get("bucket", ""),
            "context_note": r.get("context_note", ""),
            "step": int(r.get("step") or 0), "next_step": int(r.get("step") or 0) + 1,
            "last_sent_date": r.get("last_sent_date", ""),
        })
    if a.daily_cap:
        out = out[:a.daily_cap]
    print(json.dumps({"today": today, "due": out, "count": len(out)}))


def cmd_mark_sent(a):
    rows = _read(a.data_dir)
    intervals = _parse_intervals(a.intervals)
    hit = None
    for r in rows:
        if r["profile_url"] == a.url:
            step = int(r.get("step") or 0) + 1
            r["step"] = str(step)
            r["last_sent_date"] = a.date
            if step >= a.max_steps:
                r["status"] = "done"
                r["next_due_date"] = ""
            else:
                r["status"] = "active"
                # interval to the NEXT step lives at index `step`
                gap = intervals[step] if step < len(intervals) else intervals[-1]
                r["next_due_date"] = _add_days(a.date, gap)
            hit = {"profile_url": r["profile_url"], "step": step,
                   "status": r["status"], "next_due_date": r["next_due_date"]}
            break
    _write(a.data_dir, rows)
    print(json.dumps(hit or {"error": "not found", "url": a.url}))


def cmd_mark_replied(a):
    rows = _read(a.data_dir)
    hit = None
    for r in rows:
        if r["profile_url"] == a.url:
            r["status"] = "replied"
            r["next_due_date"] = ""
            r["last_checked_date"] = a.today or r.get("last_checked_date", "")
            hit = {"profile_url": r["profile_url"], "status": "replied"}
            break
    _write(a.data_dir, rows)
    print(json.dumps(hit or {"error": "not found", "url": a.url}))


def cmd_status(a):
    rows = _read(a.data_dir)
    by_status, by_bucket = {}, {}
    for r in rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
        b = r.get("bucket") or "(none)"
        by_bucket[b] = by_bucket.get(b, 0) + 1
    print(json.dumps({"total": len(rows), "by_status": by_status, "by_bucket": by_bucket}))


def main(argv=None):
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--data-dir", required=True)

    s = sub.add_parser("add-leads"); common(s); s.add_argument("--file", required=True)
    s.set_defaults(func=cmd_add_leads)

    s = sub.add_parser("due"); common(s)
    s.add_argument("--today", required=True)
    s.add_argument("--max-steps", type=int, default=3, dest="max_steps")
    s.add_argument("--intervals", default="0,4,7")
    s.add_argument("--daily-cap", type=int, default=0, dest="daily_cap")
    s.set_defaults(func=cmd_due)

    s = sub.add_parser("mark-sent"); common(s)
    s.add_argument("--url", required=True); s.add_argument("--date", required=True)
    s.add_argument("--max-steps", type=int, default=3, dest="max_steps")
    s.add_argument("--intervals", default="0,4,7")
    s.set_defaults(func=cmd_mark_sent)

    s = sub.add_parser("mark-replied"); common(s)
    s.add_argument("--url", required=True); s.add_argument("--today", default="")
    s.set_defaults(func=cmd_mark_replied)

    s = sub.add_parser("status"); common(s)
    s.set_defaults(func=cmd_status)

    a = p.parse_args(argv)
    a.func(a)


if __name__ == "__main__":
    main()
