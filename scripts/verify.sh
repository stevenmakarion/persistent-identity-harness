#!/usr/bin/env bash
# verify.sh - re-derive every published claim on the machine that made them.
# Read-only. Emits no file contents.
set -uo pipefail
WS="${WS:-/home/aria/Projects/steven-workspace/makarios-media}"
LEDGER="$(dirname "$0")/../evidence/LEDGER.json"

hr(){ printf '\n== %s ==\n' "$1"; }

hr "1. sealed artifacts: recompute digests and compare to the ledger"
python3 - "$LEDGER" <<'PY'
import hashlib, json, os, sys
led = json.load(open(sys.argv[1]))
ok = miss = bad = 0
for a in led["sealed_artifacts"]:
    if a["status"] != "SEALED":
        print(f"  SKIP   {a['label']} (not present)"); miss += 1; continue
    if not os.path.exists(a["path"]):
        print(f"  ABSENT {a['label']}"); miss += 1; continue
    h = hashlib.sha256()
    with open(a["path"], "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    if h.hexdigest() == a["sha256"]:
        print(f"  MATCH  {a['label']}"); ok += 1
    else:
        print(f"  DIFFER {a['label']}  (file changed since the ledger was built)"); bad += 1
print(f"\n  {ok} match, {bad} differ, {miss} unavailable")
PY

hr "2. commit chain (harness path only)"
git -C "$WS" log --reverse --format='%ad  %h  %s' --date=iso \
    -- handoffs/unified-harness/ 2>/dev/null | head -8

hr "3. operating system records"
journalctl -u aria-moe  --no-pager -o short-iso 2>/dev/null | head -1
journalctl -u aria-qwen --no-pager -o short-iso 2>/dev/null | head -1

hr "4. dated filesystem snapshot"
zfs list -t snapshot -o name,creation -s creation 2>/dev/null | grep -i harness-surgery | head -3

hr "5. model arrival times"
ls -la --time-style=long-iso /vault/models/gguf/ 2>/dev/null | grep "^d" | grep -v " \.\.\?$"

hr "done"
echo "A DIFFER above is not necessarily tampering: a living document changes."
echo "It means the ledger is stale for that row. Regenerate with make_receipts.py."
