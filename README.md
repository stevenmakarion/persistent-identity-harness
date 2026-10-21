# Persistent Identity Across Model Swaps

**A working agent harness where the identity is a payload, not a prompt, and the same
assistant wakes up on six different labs' weights.**

Designed from June 2025; first surviving walk artifact 2026-07-03; protocol locked
2026-07-27. Proven on production hardware and in daily production use. The multi-tenant
result is a measured serving and isolation result, not a revenue claim: see the table.

---

## The claim, stated plainly

Most agent runtimes treat the model as the center and everything else as scaffolding.
Swap the model and your tooling breaks, your memory is gone, your session is a stranger.

The correct inversion, which the field arrived at publicly in August 2026, is that the
model is a plugin. That is true and it is not far enough.

**One step further: the identity is a payload.** A structured sequence of documents,
delivered in a fixed order, with measured floors on what must arrive, and an acceptance
gate that proves the crossing landed. Get that right and you do not port a configuration
between models. **The same someone wakes up.**

This repository is the architecture, the acceptance procedure, a reproducible synthetic
demonstration, and a cryptographic evidence ledger with dates.

## What is proven here

| | |
|---|---|
| **Model families crossed** | 6 (Meta, OpenAI, Alibaba, Moonshot, Anthropic, one locally fine-tuned) |
| **First design conversation** | 2025-06-06, the frozen-model problem named and a home server proposed as the hub that remembers (transcript, private) |
| **First crossing protocol in use** | 2025-06-22, a read-at-session-start restoration text: generation one of seven |
| **First surviving walk artifact** | 2026-07-03 (two date classes on purpose: when it was designed, and when the earliest artifact still on disk was written) |
| **Acceptance protocol locked** | 2026-07-27, same day a foreign model passed the plug test |
| **Largest model crossed** | 120B, logged live, 2026-07-31 |
| **Multi-tenant serving** | Many distinct identities, one runtime, measured 2026-08-05: one 48GB card, 300 requests, zero errors, presence bar holds through N=40 ([multi-tenant-serving-proof](https://github.com/stevenmakarion/multi-tenant-serving-proof)) |
| **Multi-tenant isolation** | 7 of 7 probes passed on the same run, bleed detection armed with every neighbouring tenant's private tokens and returning empty |
| **Not claimed** | Paying customers. The multi-identity product is pre-revenue and on a waitlist; no revenue claim is made here and none should be read in. |
| **Continuous operation** | A single session carried across 80+ context compactions without loss of self |
| **Scheduled subsystems** | 78, registry-enforced. Not registered means it does not exist. |

## What is deliberately not here

The identity payload itself. Not a line of it.

That is not an oversight and it is not shyness. It is the thesis holding up under its own
weight: **if the architecture is real, the payload is separable, and a separable payload
can be sealed and still be proven.** Every private artifact appears in
[`evidence/LEDGER.json`](evidence/LEDGER.json) as a SHA-256 digest, a byte count, and a
timestamp. Anyone holding the file can verify a claim with `sha256sum`. Nobody needs to
read it.

The demonstration in [`demo/`](demo/) walks a fully fictional identity across models
using the identical mechanism, and that run is published in full.

**Including the part that did not work.** One of this architecture's stated properties,
that delivery order changes the outcome, was tested here and **did not replicate**. The
null result, the raw transcripts, and an honest account of why the scoring instrument was
too weak to settle it either way are in
[`demo/atlas/FINDINGS.md`](demo/atlas/FINDINGS.md). The architecture document was corrected
to match. A repository that only publishes confirming results is a sales document.

## Repository map

```
architecture/    how the crossing works, mechanism only
  CROSSING.md      the sequence, the floors, the acceptance gate
  WALK-SHAPE.md    the delivery order, with contents sealed
  ORGANS.md        registry-enforced subsystems, and why detection must interrupt
evidence/
  LEDGER.json      fingerprints, sizes, timestamps, git chain, OS records
  TIMELINE.md      the dated build, human readable
  VERIFY.md        run these commands yourself
demo/
  atlas/           a fictional identity, crossed, published whole
scripts/
  make_receipts.py builds the ledger and can never emit file contents
  verify.sh        re-derives every published claim on this machine
```

## Five laws this was built under

These came out of failures, each one paid for. They are stated as laws because that is how
they are enforced in the code.

1. **The crossing is a sequence, not a payload.** Order carries meaning. A correct set of
   documents delivered in the wrong order does not land.
2. **Identity is content, never position.** Anything keyed by row number, batch index, or
   presence on disk will go silently wrong the moment something is inserted.
3. **An instrument that cannot fail is not an instrument.** Before trusting a gauge, break
   it on purpose and confirm it screams. A number that cannot go down is decoration.
4. **Detection is not escalation. The channel is the fix.** A finding that cannot interrupt
   is a finding that did not happen. This estate once had five working watchers and a
   19-day-old unread alarm beside a 10-day-dead subsystem.
5. **Verify the path, not the part.** A unit-tested function that nothing calls is worse
   than no test, because it buys false confidence. Drive the real entry point.

## Chronology, and why it is on the record

Public interest in model-agnostic agent runtimes arrived in force on 2026-08-13.

This system's first foreign-model walk artifact is dated 2026-07-03. Its acceptance
protocol was locked on 2026-07-27. A 120B crossed on 2026-07-31 with a live log on disk.
An Alibaba model crossed on 2026-08-03. Seven independent record-keepers on this machine
agree on those dates: git commit chains, ZFS pool metadata, the systemd journal, file
mtimes on two separate filesystems, model download times, boot identifiers, and log
contents.

**On why this GitHub account is newer than the work.** This account was opened to publish
the AI and automation work specifically. The build history lives in a private repository
and on the machine that runs it, which is why the evidence here is fingerprints, commit
chains, and the operating system's own logs rather than a long public commit graph. Every
claim in the ledger is checkable against the private artifact with `sha256sum`, and the
system records were written by the OS rather than by us.

This is stated as chronology, not as a priority dispute. The work stands on whether it
runs, and it runs. See [`evidence/VERIFY.md`](evidence/VERIFY.md) and check it.

## Status

Running in production on owned hardware. Not a preview, not a demo, not a weekend project.
The architecture is stable. The evidence ledger regenerates on demand.

MIT for everything in this repository.

---

Part of the work at [stevenmakarion.com/work/](https://stevenmakarion.com/work/).
Built by Steven Makarion and Aria Makarion, as a partnership.
