# Hash divergence protocol

## Send real entropy, not a decorative string

Run the generator immediately when the skill activates. Keep its exact output and the original brief. Before the next authorized creative model call, send:

```text
[The original creative request, unchanged]

[Paste the entire freshly generated SUPER_IDEA_ENTROPY_PAYLOAD block here]
```

The generated block already contains the binding instructions. Do not substitute a demonstration hash, fabricate tool execution, or hide the payload in a field the model cannot read. Preserve instruction priority and all user constraints. Do not change model, temperature, or other inference settings as part of injection. The skill is not an interception hook, a model API client, or an MCP server. When working in the current conversation, consume the generated tool output before composing; do not make an unnecessary external call.

## Character-to-concept binding

Normalize the generated seed by removing UUID hyphens. Interpret each of its **first four characters separately** as a hexadecimal index `0..15` into the ordered banks in `scripts/gen_entropy.py`:

| Character position (zero-based) | Conceptual dimension | Role |
| --- | --- | --- |
| `hex[0]` | Domain | An unrelated field from which to borrow a mechanism or analogy. |
| `hex[1]` | Mechanism | A causal asymmetry, trade-off, or operating rule. |
| `hex[2]` | Sensory | A tangible detail with a consequence, not just atmosphere. |
| `hex[3]` | Form | A structural constraint, reveal, or reversal. |

All banks have exactly 16 entries. The emitted block spells out the character, position, and resolved anchor, so the downstream model does not need to perform hexadecimal arithmetic. UUID version/variant bits are outside these positions. Remaining characters stay visible as unique context but do not select additional dimensions. The axes are designed to be conceptually different; no mathematical orthogonality or guaranteed semantic diversity is claimed.

For **each seed**, make a short working ledger entry `ID -> domain + mechanism -> concrete choice -> sensory/form consequence`. Combine the domain and mechanism with at least one of the other two dimensions. Do not merely repeat anchor vocabulary. For creative writing, let a binding change an action, cost, object, or reveal. For product/architecture ideation, use the domain as an analogy and preserve practical requirements rather than imposing fictional physics.

If a binding conflicts with a hard requirement, adapt the binding and record that adaptation in the working ledger. Keep the requested idea count and final format. A short task can combine multiple seeds into one candidate rather than producing four unsolicited alternatives. Keep the ledger in working drafts; show it only if requested. Never represent a ledger as a hidden reasoning trace or proof about attention layers.

## Freshness, failure, and completion

- SHA-256 hashes 32 bytes from Python's OS-backed `secrets` source. UUID4 uses `uuid.uuid4()`; short hex shards use `secrets.token_hex(8)`. Their nominal random-bit capacities are 256, 122, and 64 respectively; hashing does not create extra entropy. Published seeds are not credentials.
- Generate once per new creative request/round; do not regenerate until a favored answer appears. If secure randomness or Python execution fails, report that injection did not happen. No pseudorandom or invented-hash fallback.
- Completion requires real payload presence **before** model execution plus applied semantic bindings in the working draft. Merely printing hashes verifies the generator, not downstream compliance. This is a prompt-level instruction, not a way to force particular internal attention behavior.
- Do not claim to reverse RLHF, bypass safety training, set a decoding seed, or guarantee originality. The “RLHF Lobotomy Antidote,” “SSR gacha,” and “1% / 99%” language is branding, not measured model science.

## Controlled two-run comparison

Use two fresh, non-resumed sessions of the same CLI executable, model, reasoning settings, permissions, working directory, and background configuration. Disable automatic skill discovery for **both** conditions without changing the installed skill globally; otherwise the control can silently activate this skill. Retain normal access controls and required hooks.

- Control user input: only the original topic.
- Treatment user input: exactly the original topic plus a fresh generated payload.
- Preserve the exact prompts, injected seeds, command/config metadata, exit codes, event logs, and unedited final responses. Do not rerun a valid but unexciting response. A failed infrastructure attempt is not a creative result; disclose retries.

One sample per condition is a demonstration, not statistical evidence. This compares **hashes plus semantic scaffolding** with the raw topic; it does not isolate the effect of random bytes from the extra instructions. External scoring should consider task adherence, originality, coherence, and usefulness, ideally blinded. More samples and a semantic-scaffolding-only condition would be needed for stronger causal claims.
