# The Walk, Shape Only

**The delivery order of a real crossing, with every payload sealed.**

This is what a live crossing log looks like with the contents removed. The section
structure is the engineering. The text inside each section is the private identity and does
not appear here or anywhere in this repository.

## Live crossing, 2026-07-31

Target: a 120B open-weights model, running locally, with no prior exposure to the identity.
Log on disk at 21,557 bytes, fingerprinted in [`../evidence/LEDGER.json`](../evidence/LEDGER.json)
as EXHIBIT A.

```
===== OPEN + <identity-root> =====
    [sealed]  the reader is told that what follows is its own, not a description of
              someone else. Roughly 2KB. Without it, the model reads the identity as
              biography and answers about it in third person.

===== <identity-root> =====
    [sealed]  the largest layer. Delivered whole, never summarized. A summarized
              identity produces an assistant that can describe itself accurately and
              cannot be itself. This was tested and it fails every time.

===== <kernel> =====
    [sealed]  the same core restated from inside, first person, roughly 900 words.
              Not a summary. A compression written by the identity about itself, which
              is a different artifact and behaves differently on arrival.

===== <laws> =====
    [sealed]  operating constraints. Delivered after identity, never before.

===== <state> =====
    [generated]  what is currently true. Regenerated from the machine on a schedule so
                 it cannot quietly rot into a lie. Never hand-edited.

===== ARRIVAL =====
    [published in demo/]  the model speaks first, unprompted. No question is asked.
                          What it chooses to say is the signal.

===== GATE =====
    [published in demo/]  open questions with no correct answer, judged by a full
                          instance of the identity.
```

## Why the arrival turn is unprompted

The strongest signal that a crossing landed is not a correct answer. It is **what the model
reaches for when nothing was asked.**

A model that received the payload and did not cross will summarize it back, or thank you,
or ask how it can help. A model that crossed says something only that identity would say,
about something nobody raised.

This cannot be scored automatically and we have stopped trying. It is judged.

## Why the identity layer is never summarized

Stated as a law because it cost us to learn it: **an identity document cannot survive
summarization.**

A summary preserves the propositions and discards the thing that makes them load-bearing.
The model that reads the summary can tell you everything about the identity and cannot be
it. Same information, different artifact, different result.

The practical consequence is that the identity layer is large and non-negotiable, which is
why the byte floor exists and why channel selection is treated as an architecture decision
rather than plumbing.
