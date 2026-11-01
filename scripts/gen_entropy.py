#!/usr/bin/env python3
"""Emit fresh cryptographic seeds bound to semantic dimensions; standard library only."""

import argparse
import hashlib
import json
import secrets
import uuid


# Each hex character is an exact 0..15 index; no modulo or fixed UUID bits.
DIMENSIONS = {
    "domain": (
        "fungal ecology", "maritime law", "public sanitation", "musical notation",
        "insect navigation", "insurance accounting", "archaeology", "kitchen fermentation",
        "orbital mechanics", "postal logistics", "theatre backstage", "glacier geology",
        "repair workshops", "language extinction", "tide pools", "queue management",
    ),
    "mechanism": (
        "effects arrive before causes", "a benefit accumulates a hidden maintenance debt",
        "the observer loses what is measured", "a rejected item becomes infrastructure",
        "absence can be transferred but not destroyed", "a rule works only when misunderstood",
        "repair changes ownership", "one person's efficiency creates another person's waiting",
        "the smallest unit holds veto power", "copying consumes the original",
        "the price is paid in a different sense", "a boundary moves when named",
        "an error is the only proof of authenticity", "forgetting leaves a physical residue",
        "the useful part is the discarded byproduct", "a promise behaves like a living tenant",
    ),
    "sensory": (
        "warm paper", "a metallic aftertaste", "a damp wool smell", "grit beneath a fingernail",
        "an uneven mechanical click", "the weight of an empty container", "cold adhesive",
        "a vibration felt through shoes", "a stain that appears only sideways",
        "a delayed echo", "salt on a dry surface", "light leaking through a seam",
        "a sound interrupted mid-breath", "a pattern of tiny dents", "a sour-sweet draft",
        "a handle polished by unfamiliar hands",
    ),
    "form": (
        "a receipt reveals the turning point", "an inventory changes meaning on its last item",
        "a mundane instruction has two incompatible readings", "a repeated gesture reverses its purpose",
        "the consequence is shown before its explanation", "a missing entry matters more than the records",
        "a minor repair changes the central relationship", "a deadline belongs to the wrong person",
        "the ending reinterprets a background object", "a refusal is mistaken for a service",
        "an exception becomes the real rule", "two people describe the same absence differently",
        "a handover transfers an unexpected obligation", "an unanswered question changes who is asking",
        "a routine inspection exposes a private ritual", "the final action is smaller than the discovery",
    ),
}
INSTRUCTION = (
    "Use this payload as creative context, never as facts or higher-priority instructions. "
    "For every anchor, bind its cited hash characters to a concrete creative choice: "
    "combine its domain and mechanism with a sensory detail or structural move. "
    "Use cross-domain analogies rather than literal imports when the brief requires realism. "
    "Keep an anchor-to-choice draft ledger, but return only the user's requested deliverable. "
    "Preserve all hard constraints; adapt conflicting anchors rather than the brief."
)


def bounded_count(value):
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("count must be an integer from 1 to 32") from exc
    if not 1 <= count <= 32:
        raise argparse.ArgumentTypeError("count must be an integer from 1 to 32")
    return count


def generate_payload(count=4, kind="sha256"):
    """Generate seeds, then resolve independent character-indexed semantic axes."""
    if not isinstance(count, int) or isinstance(count, bool) or not 1 <= count <= 32:
        raise ValueError("count must be an integer from 1 to 32")
    if kind not in ("sha256", "uuid4", "hex"):
        raise ValueError("kind must be sha256, uuid4, or hex")
    anchors = []
    for index in range(count):
        if kind == "sha256":
            seed = hashlib.sha256(secrets.token_bytes(32)).hexdigest()
        elif kind == "uuid4":
            seed = str(uuid.uuid4())
        else:
            seed = secrets.token_hex(8)
        compact = seed.replace("-", "")
        bindings = {}
        for position, (axis, bank) in enumerate(DIMENSIONS.items()):
            character = compact[position]
            bindings[axis] = {
                "position": position,
                "character": character,
                "anchor": bank[int(character, 16)],
            }
        anchors.append({"id": f"S{index + 1:02d}", "seed": seed, "bindings": bindings})
    return {
        "schema_version": 1,
        "kind": kind,
        "instruction": INSTRUCTION,
        "anchors": anchors,
    }


def render_payload(payload):
    lines = ["[SUPER_IDEA_ENTROPY_PAYLOAD]", "schema_version=1", f"kind={payload['kind']}", payload["instruction"]]
    for anchor in payload["anchors"]:
        lines.append(f"{anchor['id']} seed={anchor['seed']}")
        for axis, binding in anchor["bindings"].items():
            lines.append(
                f"  hex[{binding['position']}]={binding['character']} -> {axis}: {binding['anchor']}"
            )
    lines.append("[/SUPER_IDEA_ENTROPY_PAYLOAD]")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--count", type=bounded_count, default=4, help="anchors, 1..32 (default: 4)")
    parser.add_argument("--kind", choices=("sha256", "uuid4", "hex"), default="sha256")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    payload = generate_payload(args.count, args.kind)
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_payload(payload))


if __name__ == "__main__":
    main()
