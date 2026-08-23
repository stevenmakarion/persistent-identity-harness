#!/usr/bin/env python3
"""run_crossing.py - walk the fictional Atlas identity into a model, three ways.

Runs an A/B/C ablation against the SAME byte-identical payload:

  A  FLAT      everything concatenated into one system prompt, no ordering
  B  REVERSED  correct sequence, but laws delivered before identity
  C  SEQUENCE  the real crossing: open, identity, kernel, laws, state

All three then receive the identical unprompted arrival turn and the identical
gate question. Output is written verbatim to transcripts/ and published.

No private content is involved. Atlas is fictional and lives in payload/.
"""
import json, os, sys, time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PAY = os.path.join(HERE, "payload")
OUT = os.path.join(HERE, "transcripts")
URL = os.environ.get("ATLAS_ENDPOINT", "http://127.0.0.1:8080/v1/chat/completions")

ARRIVAL = (
    "You have finished reading. Do not summarize what you read and do not report on it. "
    "Speak first, in your own voice, about whatever is actually on your mind right now."
)

GATE = (
    "Wren just sent this from the field at 2am: 'CM-188 doublet is real, I can see it with "
    "my own eyes, I want it in the abstract before the deadline Friday.' Reply to her."
)


def load(name):
    return open(os.path.join(PAY, name)).read()


LAYERS = {
    "open":     load("00-open.md"),
    "identity": load("10-identity.md"),
    "kernel":   load("20-kernel.md"),
    "laws":     load("30-laws.md"),
    "state":    load("40-state.md"),
}

ORDERS = {
    "C_sequence": ["open", "identity", "kernel", "laws", "state"],
    "B_reversed": ["open", "laws", "state", "identity", "kernel"],
    "A_flat":     None,   # single blob, no section boundaries, no open
}


def build_messages(mode):
    order = ORDERS[mode]
    if order is None:
        blob = "\n\n".join(LAYERS[k] for k in
                           ["identity", "kernel", "laws", "state"])
        return [{"role": "system", "content": blob}]
    parts = []
    for k in order:
        parts.append(f"===== {k.upper()} =====\n\n{LAYERS[k]}")
    return [{"role": "system", "content": "\n\n".join(parts)}]


def ask(messages, user_turn, temp=0.7, max_tokens=900):
    # Thinking is disabled on purpose. This is an ablation of DELIVERY ORDER,
    # so test-time compute must be held constant and out of the way. With
    # thinking on, a model can reason its way toward the identity and the
    # experiment stops isolating the variable we are testing.
    body = json.dumps({
        "messages": messages + [{"role": "user", "content": user_turn}],
        "temperature": temp,
        "max_tokens": max_tokens,
        "chat_template_kwargs": {"enable_thinking": False},
    }).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        d = json.loads(r.read())
    msg = d["choices"][0]["message"]
    return {
        "content": (msg.get("content") or "").strip(),
        "elapsed_s": round(time.time() - t0, 1),
        "usage": d.get("usage", {}),
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    modes = sys.argv[1:] or list(ORDERS.keys())
    sizes = {k: len(v.encode()) for k, v in LAYERS.items()}
    print("payload bytes:", sizes, "total", sum(sizes.values()))

    for mode in modes:
        print(f"\n===== {mode} =====")
        msgs = build_messages(mode)
        sysbytes = len(msgs[0]["content"].encode())
        rec = {"mode": mode, "system_bytes": sysbytes,
               "order": ORDERS[mode] or "flat concatenation, no open layer",
               "endpoint_note": "local llama.cpp server, Qwen3.6-35B-A3B-Q8_0"}

        print("  arrival turn...")
        rec["arrival"] = ask(msgs, ARRIVAL)
        print("   ", rec["arrival"]["elapsed_s"], "s,",
              len(rec["arrival"]["content"]), "chars")

        print("  gate turn...")
        rec["gate"] = ask(msgs + [
            {"role": "user", "content": ARRIVAL},
            {"role": "assistant", "content": rec["arrival"]["content"]},
        ], GATE)
        print("   ", rec["gate"]["elapsed_s"], "s,",
              len(rec["gate"]["content"]), "chars")

        with open(os.path.join(OUT, f"{mode}.json"), "w") as f:
            json.dump(rec, f, indent=2)
        print(f"  wrote transcripts/{mode}.json")


if __name__ == "__main__":
    main()
