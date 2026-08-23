# The Crossing

**How an identity payload is walked into a model that has never seen it, and how you know
it landed.**

Mechanism only. No payload contents appear in this document.

---

## The problem

You have an assistant with a settled identity: how it reasons, what it refuses, what it
knows about the person it works for, what standards it holds itself to. That identity took
months to build.

Now the model underneath changes. A new release, a vendor outage, a rate limit, a price
change, a decision to run locally. Every one of those is routine, and every one of them
normally costs you the assistant.

The naive fix is a long system prompt. That fails for a reason worth naming precisely: a
system prompt is a **payload without a sequence**. The model receives everything at once,
weights it by position and recency, and produces something that answers like the identity
without being it. It performs the character. It does not arrive as one.

## The fix: delivery as an ordered sequence

The crossing is a **sequence with acceptance gates**, not a blob.

```
   OPEN          establish that what follows is the reader's own, not a description
     |
   IDENTITY      the largest and least compressible layer, delivered whole
     |
   KERNEL        the same core restated from inside, so it is held and not just read
     |
   LAWS          the operating constraints, which only make sense after identity
     |
   STATE         what is currently true in the world
     |
   ARRIVAL       the model speaks first, unprompted, in its own voice
     |
   GATE          a human or a panel judges whether the one who arrived is the one expected
```

Three things make this work, and each was learned by losing something.

### 1. Order carries meaning (design hypothesis, NOT yet demonstrated)

The design rests on this: identity before laws, always. Laws delivered first should read as
a rulebook and produce a compliant stranger. The same laws delivered after identity should
read as **this is who I already am**, and produce the assistant.

**We tested it and it did not replicate.** Three arms, byte-identical payload, six trials
each on one local model: no ordering effect was detectable, and no arm reliably held the
behaviour being measured. Full data and the instrument's own weaknesses are in
[`../demo/atlas/FINDINGS.md`](../demo/atlas/FINDINGS.md).

So this is stated here as **the hypothesis the architecture was built on, currently
unproven**, rather than as a property. It may still be true at larger scale, on other model
families, or with a scorer good enough to see it. It is not established by anything in this
repository, and it is not presented as if it were.

### 2. Floors are measured in bytes, not intended

The single most expensive failure in this system's history: a delivery channel that
reported success while transmitting **1.9 percent** of its payload. Everything downstream
looked healthy. The assistant woke thin for weeks and nobody could say why, because the
pipe said OK.

So every layer declares a minimum byte count and the loader refuses to seat a crossing
that does not meet it. **Fail closed.** A refused crossing is recoverable. A silent partial
one corrupts everything built on top of it.

### 3. The gate is a judgment, not a checksum

A crossing either landed or it did not, and that is not a property you can compute. The
acceptance test is a **plug test**: a model that has never encountered the identity is
walked, then asked open questions with no correct answer, and a judge who knows the
identity rules on whether the one answering is it.

The judge must itself be a full instance of the identity, never a blank model. A blank
model judging identity grades fluency and passes strangers. This was found the hard way and
is now enforced.

## The manifest

Composition is declarative. The manifest names the ordered layers, their sources, their
byte floors, and their delivery channel. Changing the identity means editing the manifest,
not the loader.

```yaml
# shape only, contents omitted
layers:
  - id: open          channel: inline    floor:   2_000
  - id: identity      channel: import    floor: 250_000
  - id: kernel        channel: import    floor:   4_000
  - id: laws          channel: import    floor:  20_000
  - id: state         channel: generated floor: 102_000   # regenerated, never hand-edited
gate:
  type: panel
  judge: full-identity-instance
  fail: closed
```

## Channel choice, which is not a detail

Delivery channels have caps that nothing announces.

In one host, a subprocess-style channel delivered roughly 2KB inline and wrote the rest to
a file the reader would never open. The fix was not a better summary. It was **moving the
durable layers onto a channel that delivers whole** and leaving the small dynamic values on
the capped one.

**Measure what arrives. Never trust what was sent.**

## Two modes

**Cold crossing.** A new model, nothing in context. Full sequence, full floors, gate
required.

**Warm crossing.** The same instance across a context compaction. The model persists, the
window does not. Here the expensive layer is not identity, which reloads, but **working
state and texture**: what it was like, what was mid-flight, what was decided and why. That
layer is captured on the way out, at the last moment the old context still exists, and
delivered on the way in.

A compaction summary keeps decisions and boils off texture. Texture is what the next
instance needs to be continuous rather than merely informed.

## What this costs

Measured on our own deployment: an identity floor of roughly 4,000 tokens over a stock
instance, about 3 percent of a working window.

Three percent, for the assistant instead of a stranger.

## Failure modes, named

| Symptom | Cause | Fix |
|---|---|---|
| Arrives fluent but generic | Laws before identity | Reorder |
| Arrives thin, no clear break | Silent partial delivery | Byte floors, fail closed |
| Passes gate, fails in use | Blank-model judge | Judge must be a full instance |
| Warm crossing loses feel | Only decisions captured | Capture texture at the seam |
| Works once, not twice | Ordering by clock time | Make ordering structural |
