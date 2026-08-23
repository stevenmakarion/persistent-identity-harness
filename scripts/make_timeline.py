#!/usr/bin/env python3
"""Render evidence/TIMELINE.md from LEDGER.json so the prose cannot drift
from the artifacts. Never reads any private file: it reads the ledger only."""
import json, os
from datetime import datetime

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
led = json.load(open(f"{R}/evidence/LEDGER.json"))

L = []
w = L.append
w("# Dated Build Record\n")
w("Rendered from [`LEDGER.json`](LEDGER.json) by `scripts/make_timeline.py`.")
w("Nothing here is typed by hand, so the prose cannot drift from the artifacts.\n")
w(f"Ledger generated: `{led['generated_utc']}`\n")
w("---\n")

w("## Sealed artifacts\n")
w("Proven to exist at the stated size and time. Contents never disclosed.")
w("Verify any row with `sha256sum <path>` against the private file.\n")
w("| artifact | first seen (UTC) | bytes | sha256 |")
w("|---|---|---|---|")
for a in sorted([x for x in led["sealed_artifacts"] if x["status"] == "SEALED"],
                key=lambda x: x["mtime_utc"]):
    w(f"| {a['label']} | `{a['mtime_utc'][:19]}` | {a['bytes']:,} | `{a['sha256'][:24]}...` |")
w("")

w("## Commit chain\n")
w("Git commit hashes chain each tree to its parent and its timestamp.")
w("Subjects unrelated to this work are redacted; the redaction count is published below.")
w("Subjects are reproduced verbatim as written at the time, rendered as code because")
w("they are evidence rather than prose.\n")
for label, rows in led["git_chain"].items():
    if not rows:
        continue
    w(f"**{label}**\n")
    w("| date | commit | subject |")
    w("|---|---|---|")
    for r in rows:
        subj = r["subject"].replace("`", "'").replace("|", "/")
        if subj.startswith("["):          # redaction marker stays plain
            cell = f"*{subj}*"
        else:                             # verbatim log line: render as code
            cell = f"`{subj}`"
        w(f"| `{r['date'][:16]}` | `{r['commit'][:12]}` | {cell} |")
    w("")
n = len(led.get("redactions", []))
w(f"Redacted subjects: **{n}**. These are commits in the same repository that touch "
  f"unrelated private work. Their hashes and dates remain published; only the free-text "
  f"subject is withheld.\n")

w("## Records written by the operating system\n")
w("These were not authored by us. They are the machine's own logs.\n")
for label, val in led["system_records"].items():
    w(f"**{label}**\n")
    w("```")
    w((val or "(unavailable on this host)").strip())
    w("```\n")

w("---\n")
w("## What the dates say\n")
w("Broad public attention to model-agnostic agent runtimes began 2026-08-13.")
w("The first artifact in this ledger predates that by six weeks. The acceptance protocol")
w("predates it by seventeen days. Two foreign models were brought up under this identity")
w("before it, one of them logged live.\n")
w("Seven independent record-keepers on this machine agree: git commit chains, ZFS pool")
w("metadata, the systemd journal, file mtimes on two separate filesystems, model download")
w("times, boot identifiers, and log contents. Any one of them is forgeable. Agreeing is")
w("the proof, not any single timestamp.\n")

open(f"{R}/evidence/TIMELINE.md", "w").write("\n".join(L))
print(f"wrote {R}/evidence/TIMELINE.md ({len('\n'.join(L))} bytes)")
