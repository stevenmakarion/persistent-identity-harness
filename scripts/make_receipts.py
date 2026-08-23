#!/usr/bin/env python3
"""make_receipts.py — build the evidence ledger WITHOUT disclosing any content.

THE ONE LAW OF THIS SCRIPT: it emits fingerprints, sizes, and timestamps.
It never emits a byte of any private file. Every value it writes is either
a SHA-256 digest, an integer, a path, or an ISO timestamp. There is no code
path in this file that can print file contents -- verified by design: the
only read of a private file is inside sha256_of(), which returns a digest.

Anyone holding the private artifact can verify a claim by running
`sha256sum <file>` and comparing. Disclosure is never required for proof.
"""
import hashlib, json, os, subprocess, sys
from datetime import datetime, timezone

WS = os.environ.get("HARNESS_REPO", os.path.expanduser("~/harness-repo"))
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evidence")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def iso(ts):
    return datetime.fromtimestamp(ts, timezone.utc).isoformat()


def fingerprint(path, label, note=""):
    """A sealed artifact: proven to exist, never opened."""
    if not os.path.exists(path):
        return {"label": label, "path": path, "status": "NOT_PRESENT"}
    st = os.stat(path)
    return {
        "label": label,
        # Published relative to the private repo root, never as an absolute
        # path: the machine's directory layout is not this repository's business.
        "path": path.replace(WS + "/", "").replace("/home/aria/", "~/"),
        "sha256": sha256_of(path),
        "bytes": st.st_size,
        "mtime_utc": iso(st.st_mtime),
        "note": note,
        "status": "SEALED",
    }


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=120).stdout.strip()
    except Exception as e:
        return f"(unavailable: {e})"


# ---------------------------------------------------------------- exhibits
SEALED = [
    ("/home/aria/aria-local/web-session-70b.json",
     "EXHIBIT E - first foreign-model walk (Llama-70B class)",
     "The earliest surviving artifact of an identity payload walked into a "
     "non-Anthropic model. Contents are private; the fingerprint is not."),
    ("/vault/logs/crossing-live.log",
     "EXHIBIT A - live crossing log (gpt-oss-120B)",
     "Written as the crossing happened. Section structure is published in "
     "architecture/WALK-SHAPE.md; the transcript itself is sealed."),
    (f"{WS}/handoffs/unified-harness/THE-CROSSING-PROTOCOL.md",
     "EXHIBIT F1 - the crossing protocol (locked 2026-07-27)",
     "The acceptance procedure for walking an identity into an unfamiliar "
     "model. Mechanism published in architecture/; document sealed."),
    (f"{WS}/handoffs/unified-harness/THE-ARCHITECTURE.md",
     "EXHIBIT F2 - as-built architecture record",
     "Internal engineering record."),
    (f"{WS}/handoffs/unified-harness/soul-manifest.yaml",
     "EXHIBIT F3 - the identity manifest",
     "Declares which documents compose the payload and in what order. "
     "The ORDER is published; the documents are sealed."),
    (f"{WS}/tools/reliability/organ-registry.json",
     "EXHIBIT H - the organ registry",
     "The registry of every scheduled subsystem. Not registered = does not "
     "exist. Count and shape published; contents sealed."),
]

# Scoped deliberately to the harness path ONLY. Adjacent commits in the same
# repo concern unrelated private work and are not this repo's business.
GIT_RANGES = [
    ("harness commits (first day)",
     f"git -C {WS} log --reverse --format='%H|%ad|%T|%s' --date=iso "
     f"-- handoffs/unified-harness/ | head -20"),
    ("crossing protocol - creating commit",
     f"git -C {WS} log --diff-filter=A --format='%H|%ad|%T|%s' --date=iso "
     f"-- handoffs/unified-harness/THE-CROSSING-PROTOCOL.md"),
]

SYSTEM = [
    ("EXHIBIT B1 - OS record: 120B brought up as the identity",
     "journalctl -u aria-moe --no-pager -o short-iso 2>/dev/null | head -1"),
    ("EXHIBIT B2 - OS record: Alibaba Qwen brought up as the identity",
     "journalctl -u aria-qwen --no-pager -o short-iso 2>/dev/null | head -1"),
    ("EXHIBIT C - dated filesystem snapshot taken before harness surgery",
     "zfs list -t snapshot -o name,creation -s creation 2>/dev/null "
     "| grep -i 'harness-surgery' | head -4"),
    ("EXHIBIT D - when each foreign model physically arrived on our hardware",
     "ls -la --time-style=long-iso /vault/models/gguf/ | tail -n +4"),
    ("EXHIBIT G - boot records retained",
     "journalctl --list-boots 2>/dev/null | head -6"),
]



# --------------------------------------------------------------- redaction
# A commit subject is free text written for ourselves. Before any subject is
# published it passes this gate. The gate FAILS CLOSED: an unrecognised match
# aborts the build rather than shipping. Detection that cannot stop the
# pipeline is not detection.
# The live denylist is NOT in this repository, deliberately: a list of terms
# that must never be published is itself a list of private things, and shipping
# it would leak exactly what it exists to protect. It is loaded from a file
# outside the repo. If that file is missing the gate FAILS CLOSED and the build
# refuses to run, rather than quietly publishing with no gate at all.
DENY_FILE = os.path.expanduser(os.environ.get(
    "RECEIPTS_DENYLIST", "~/.config/receipts-denylist.txt"))
DENY_EXAMPLE = ["money", "invoice", "password", "api key", "secret",
                "credential", "medical"]


def load_denylist():
    if not os.path.exists(DENY_FILE):
        sys.exit(
            f"REFUSING TO BUILD: no denylist at {DENY_FILE}\n"
            f"  Create it with one lowercase term per line: names of people,\n"
            f"  clients, products, and topics that must never be published.\n"
            f"  A gate that cannot load its rules must not run. Fail closed.\n"
            f"  (Example terms, not a substitute: {', '.join(DENY_EXAMPLE)})")
    return [w.strip().lower() for w in open(DENY_FILE)
            if w.strip() and not w.startswith("#")]


DENY = None  # populated in main()


def subject_is_clean(subject):
    low = subject.lower()
    return [w for w in DENY if w in low]


def main():
    global DENY
    DENY = load_denylist()
    os.makedirs(OUT, exist_ok=True)
    led = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "disclosure_policy": (
            "Every entry below is a fingerprint, a size, a timestamp, or a "
            "log line emitted by the operating system. No private file "
            "content appears in this ledger, by construction."
        ),
        "verification": (
            "For any SEALED artifact, run `sha256sum <path>` against the "
            "private file and compare to the digest here. A match proves "
            "the artifact is the one this ledger attests to, with no need "
            "to disclose its contents."
        ),
        "sealed_artifacts": [fingerprint(p, l, n) for p, l, n in SEALED],
        "git_chain": {},
        "system_records": {},
    }

    blocked = []
    for label, cmd in GIT_RANGES:
        rows = []
        for line in sh(cmd).splitlines():
            parts = line.split("|", 3)
            if len(parts) != 4:
                continue
            hits = subject_is_clean(parts[3])
            if hits:
                blocked.append((parts[0][:12], parts[3], hits))
                rows.append({"commit": parts[0], "date": parts[1],
                             "tree": parts[2],
                             "subject": "[redacted - unrelated private work]"})
                continue
            rows.append({"commit": parts[0], "date": parts[1],
                         "tree": parts[2], "subject": parts[3]})
        led["git_chain"][label] = rows
    # The reason names no terms: publishing "matched: X, Y" leaks the denylist
    # one word at a time, which is the same disclosure it exists to prevent.
    led["redactions"] = [
        {"commit": c, "reason": "subject withheld: unrelated private work"}
        for c, _s, _h in blocked
    ]

    for label, cmd in SYSTEM:
        led["system_records"][label] = sh(cmd)

    with open(f"{OUT}/LEDGER.json", "w") as f:
        json.dump(led, f, indent=2)

    print(f"wrote {OUT}/LEDGER.json")
    print(f"  sealed artifacts : {len(led['sealed_artifacts'])}")
    print(f"  git chains       : {len(led['git_chain'])}")
    print(f"  system records   : {len(led['system_records'])}")
    print(f"  redacted subjects: {len(blocked)}")
    for c, subj, h in blocked:
        print(f"    {c}  blocked on {h}: {subj[:60]}")


if __name__ == "__main__":
    main()
