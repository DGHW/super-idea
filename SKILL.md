---
name: super-idea
description: Inject cryptographic random hashes and orthogonal entropy anchors into outbound prompts to break RLHF mode collapse and unlock extreme creative divergence. Use when executing creative writing, brainstorming, novel product ideation, unconventional architecture design, or any task requiring non-obvious, out-of-distribution ideas.
---

# Super Idea / 超级想法

1. **Generate entropy.** Immediately run `python scripts/gen_entropy.py --count 4` from this skill's directory, or use its absolute script path. Use real, fresh output; report execution/randomness failure instead of inventing hashes.
2. **Mutate the outbound request.** Read [references/hash_divergence_protocol.md](references/hash_divergence_protocol.md), then embed the generated `[SUPER_IDEA_ENTROPY_PAYLOAD]` block directly alongside the user's unchanged creative request **before** sending it to the authorized downstream model. If no downstream call is needed, use the generated tool output as current context before creating the answer. Apply the character-bound dimensions while preserving the user's constraints and requested format; the technique is a heuristic, not a proven RLHF cure.
