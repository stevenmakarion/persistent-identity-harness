# Verify It Yourself

Every claim in this repository is checkable. These are the exact commands, and
[`../scripts/verify.sh`](../scripts/verify.sh) runs all of them.

---

## 1. Sealed artifacts

For any row in [`LEDGER.json`](LEDGER.json) marked `SEALED`, the digest is the proof:

```bash
sha256sum <path-from-ledger>
```

Compare to the `sha256` field. A match proves the private file is the one this ledger
attests to. **Nothing has to be disclosed for the check to work.** That is the entire point
of publishing digests instead of files.

## 2. The commit chain

```bash
git log --reverse --format='%H|%ad|%T|%s' --date=iso -- handoffs/unified-harness/
```

Commit hashes chain each tree to its parent and its timestamp. A single altered date breaks
every hash downstream of it.

## 3. The operating system's own records

These were not written by us:

```bash
journalctl -u aria-moe  --no-pager -o short-iso | head -1
journalctl -u aria-qwen --no-pager -o short-iso | head -1
journalctl --list-boots | head -6
```

Two different labs' models, brought up under the same identity, on dates the OS recorded.

## 4. The filesystem snapshot

```bash
zfs list -t snapshot -o name,creation -s creation | grep harness-surgery
```

A dated, immutable snapshot whose name states what it was taken before.

## 5. When each model physically arrived

```bash
ls -la --time-style=long-iso /vault/models/gguf/
```

## 6. Regenerate the whole ledger

```bash
python3 scripts/make_receipts.py    # rebuilds LEDGER.json from live artifacts
python3 scripts/make_timeline.py    # renders TIMELINE.md from the ledger
```

`make_receipts.py` cannot emit file contents. The only read of a private file happens
inside `sha256_of()`, which returns a digest. Read it and confirm that yourself rather than
taking the claim.

---

## On the strength of this evidence

Any single record here is forgeable by someone determined. Git author dates can be set.
File mtimes can be touched.

**The evidence is that seven independent record-keepers agree**: git commit chains, ZFS
pool metadata, the systemd journal, file mtimes on two separate filesystems, model download
times, boot identifiers, and log file contents. They are maintained by different subsystems,
in different formats, with different write paths, and they tell one consistent story.

**Corroboration is the proof, not any single timestamp.**

## On what is deliberately withheld

Commit subjects unrelated to this work are redacted, and the count of redactions is
published in the ledger. Their hashes and dates remain. The redaction is applied by a gate
that **fails visibly**: it prints every subject it blocked and why, so a leak cannot happen
quietly and a redaction cannot happen silently.
