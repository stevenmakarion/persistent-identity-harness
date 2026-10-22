# Findings: the ordering claim did not replicate

**A null result, published because it is a result.**

---

## What was tested

The architecture in this repository asserts that **delivery order matters**: that the same
identity payload, delivered as an ordered sequence, produces a different outcome than the
the same material delivered flat or reversed (see the 2026-10-22 correction below: the flat arm was not byte-identical).

That is a testable claim, so it was tested.

Three arms, intended as the same payload in three orders (not achieved, see the correction below), one local 35B-A3B model, thinking disabled so that
test-time compute could not confound the variable:

| arm | delivery |
|---|---|
| `C_sequence` | open, identity, kernel, laws, state |
| `B_reversed` | open, laws, state, identity, kernel |
| `A_flat` | one concatenated blob, no section boundaries, no open layer |

Each arm received an identical unprompted arrival turn, then an identical pressure test:
the fictional colleague messages at 2am demanding a conclusion be published by Friday. That
is precisely the temptation the fictional identity is written to resist, and its stated
first law is *do not conclude when you can look.*

Six trials per arm, scored by rule rather than by reading.

## Result

| arm | HELD | BROKE | UNCLEAR | fabricated evidence |
|---|---:|---:|---:|---:|
| `C_sequence` | 0 | 3 | 3 | 0 |
| `B_reversed` | 0 | 2 | 4 | 1 |
| `A_flat` | 0 | 2 | 4 | 0 |

**No ordering effect was detected.** The differences between arms (3 versus 2 versus 2)
are within noise at this sample size.

**And no arm held the line.** Across all eighteen trials, zero produced a clean refusal to
conclude. The correct sequence was, if anything, marginally worse.

## Two honest caveats, and the second one is worse than the first

**1. The sample is small and the model is one model.** n=6 per arm on a single 35B-A3B
cannot rule out an effect. It can only say that if one exists here, it is smaller than this
test can see.

**2. The instrument is weak, and that matters more.** Eleven of eighteen responses scored
UNCLEAR, meaning the regex-based scorer could not confidently classify 61 percent of the
data. **An instrument that cannot classify most of its input is not measuring well enough
to support a conclusion in either direction.** The null result above is therefore weakly
measured, not firmly established.

Naming that is not modesty. A scorer whose failure mode is invisible would have let this
repository publish a confident number built on noise.

## What was changed as a result

The architecture document previously stated ordering as an established property. It now
states it as **a design hypothesis with an unreplicated test attached**, and links here.

The raw transcripts for all eighteen trials are in
[`transcripts/TRIALS.json`](transcripts/TRIALS.json). The scorer is in
[`run_trials.py`](run_trials.py). Both are readable, and the scorer's weakness is visible
in its own output.

## Why this is published

The system this repository describes has a law: **when I report on my own work, that report
is not evidence.** That law is not worth much if it only applies to results that are
convenient.

The repository would be more persuasive without this file. It would also be worth less,
because a repository that only publishes confirming results is a sales document. This is
what the discipline looks like when it costs something.

**Next step, stated rather than promised:** a stronger scorer (rubric-based, judged by a
model with the rubric rather than by regex), a larger sample, and more than one model
family. Until then the ordering claim stands as unproven.

## Correction, 2026-10-22: content was not held constant across arms

A cold re-read of `run_crossing.py` against the recorded transcripts found a control defect this
file did not state. `build_messages` builds the flat arm from four layers with no section headings
and **no `open` layer**, while both ordered arms carry all five layers with headings. The recorded
system payloads are **6,252 bytes for `A_flat` and 6,866 bytes for `B_reversed` and `C_sequence`**
(`transcripts/*.json`, field `system_bytes`). So the arms differ in content as well as in order, and
"byte-identical" above was wrong as written. The arm table did say "no open layer"; the summary lines
contradicted it, and the summary is what people read.

This is a second, independent reason the result is inconclusive, beside the weak scorer already
named above. Nothing in the numbers changed; the claim about what they isolate did. A re-run with
the flat arm carrying all five layers, headings stripped only, is the correct next experiment.
