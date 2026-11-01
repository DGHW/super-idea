# super-idea · 超级想法

### Stop rolling the same idea. Pull a different thread of possibility.
### 别再抽到同一个答案。让下一次想法，走另一条路。

![Agent Skill](https://img.shields.io/badge/AI_Agent-Skill-7c3aed)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab)
![Dependencies](https://img.shields.io/badge/runtime_dependencies-0-brightgreen)
![Codex CLI](https://img.shields.io/badge/Codex_CLI-ready-black)
![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-d97757)

**The “RLHF Lobotomy Antidote.” The “Latent Space Gacha Unlocker.”**
**你的「潜空间 SSR 抽卡引擎」：超级想法 / AI 创意抽卡。**

The pitch: leave the familiar **“1% probability basin”** and explore the **“99% creative frontier.”** The reality: those numbers are a metaphor, not measured probabilities. This Agent Skill adds fresh cryptographic hashes **and actionable semantic anchors** to a creative prompt. It does not remove RLHF, bypass safeguards, control internal attention, or guarantee better writing.

一句话：不是往提示词里撒乱码，而是把随机哈希的具体字符，绑定到**跨领域知识 × 因果机制 × 感官细节 × 叙事结构**。让 AI 有明确的新方向可走，而不只是把“请更有创意”再说一遍。宣传词很疯，效果判断要冷静：这是一种创意发散方法，不是已证实的“RLHF 解药”。

[Install / 安装](#install--安装) · [Try it / 开抽](#try-it--开抽) · [How it works / 原理](#how-it-works--原理) · [Benchmark / 对照测试](#benchmark--对照测试)

## Before / After: Mode Collapse vs. Black-Swan Divergence

*Illustrative directions, not benchmark results or guaranteed outputs. 以下是方向示意，不是实测结论。*

| | Standard Prompt — Mode Collapse / Cliché | Super Idea Hash-Perturbed Prompt — Black-Swan Divergence |
| --- | --- | --- |
| Creative writing / 创意写作 | “A future city trades memories; someone discovers love.” | “Postal logistics + copying consumes the original + warm paper + a receipt reveal” supplies concrete causal and sensory constraints. |
| Product ideation / 产品脑暴 | “An AI-powered productivity app.” | “Repair workshops + maintenance debt + a handover obligation” suggests a different service model to test. |
| Prompt engineering / 提示词工程 | “Be more original. Think outside the box.” | Exact hash characters resolve to named dimensions and must affect a creative choice. |
| Divergent thinking / 发散思维 | Different adjectives around one familiar premise. | Different mechanisms, costs, objects, and structures; still subject to the original brief. |

## Install / 安装

Python 3.9+ is the only runtime requirement. No pip packages, API key, network connection, MCP server, or model SDK is needed **to generate a payload**. Calling a downstream model still requires that model's normal access.

把仓库放进你的 Agent 技能目录。Codex CLI / Claude Code / 通用 Agent 技能目录任选其一；同一个工具支持多个路径时，通常装一份即可。

```text
# Codex CLI
git clone https://github.com/DGHW/super-idea.git ~/.codex/skills/super-idea

# Claude Code Skill
git clone https://github.com/DGHW/super-idea.git ~/.claude/skills/super-idea

# Shared agent skill directory, where supported
git clone https://github.com/DGHW/super-idea.git ~/.agents/skills/super-idea
```

Windows PowerShell: use `"$HOME/.codex/skills/super-idea"` (or the matching Claude/Agents path) as the destination. Do not overwrite an existing installation. Reload skill discovery or start a new agent session if the skill is not yet visible.

## Try it / 开抽

```text
Use $super-idea to write a science-fiction story about a city that sells
farewells that have not happened yet. Keep it concrete, coherent, and surprising.
```

```text
用 super-idea（超级想法）构思三个非共识产品方向。
预算不超过一万元，不收集个人信息，不要套壳聊天机器人。
```

Or generate the outbound prompt payload yourself / 手动生成载荷：

```text
python scripts/gen_entropy.py --count 4
python scripts/gen_entropy.py --count 4 --kind uuid4
python scripts/gen_entropy.py --count 4 --kind hex --format json
```

Use `python3` or `py -3` if that is your local Python launcher. Counts are limited to `1..32` to bound prompt size. Paste the **actual output** after your original creative request, before sending it to the model. The opening marker is `[SUPER_IDEA_ENTROPY_PAYLOAD]`.

## How it works / 原理

**Cryptographic random hashes → character bindings → semantic constraints → actual creative choices.**

1. SHA-256 of 32 secure random bytes, UUID4, or a 64-bit hex entropy shard.
2. Four specific hex characters independently select four different conceptual dimensions.
3. Every seed contributes a concrete choice, not just background noise.
4. Preserve the brief, merge duplicate ideas, and return the requested format.

This is **Stochastic Entropy Injection** at the prompt level. Hashing does not create more entropy. Semantic bindings are instructions the model may follow, not a proven way to force its attention layers. With a deterministic decoder, a changed prompt can still lead to a changed output; this tool does not change the decoder's random seed.

“打破大模型同质化 / Cure Mode Collapse” is the aspiration, not a validated outcome. [Read the hash divergence protocol](references/hash_divergence_protocol.md) for mapping, placement, failure handling, and honest evaluation. The root [SKILL.md](SKILL.md) is deliberately just a two-step Minimal Router: generate, then inject.

## Benchmark / 对照测试

```text
python -m unittest discover -s tests -v
```

The tests verify secure source calls, exact character-to-dimension binding, payload formats, input bounds, fresh output, and failure propagation. They do **not** score creativity.

For a writing A/B demo, run the same local `codex exec` command in two fresh sessions: one with the raw topic, one with that exact topic plus a fresh payload. Keep model/settings equal and disable automatic skill discovery in both conditions to avoid contaminating the control. Preserve raw outputs for independent scoring. This is two runs total, not two pairs.

两次生成、每组一个样本，不能证明统计显著性；处理组多了“哈希 + 语义引导”，也不能把差异全部归因于哈希。别挑结果，别修稿后假装原始输出，别把演示包装成科学证明。

## Agent Skill, not another platform / 是技能，不是新平台

- Works as a file-based **AI Agent Skill / Claude Code Skill / Codex CLI** workflow.
- **MCP** is not required; an existing MCP-enabled agent can still use the generated text. This repo does not implement an MCP server.
- No model patching, safety bypass, background daemon, or automatic prompt interception.
- Local generation is offline; outbound prompts go only through your existing authorized model tool.

**If this opens a new creative direction, star it and share the exact prompt + seed + output—not just a cherry-picked screenshot.**

**抽到好想法就点颗 Star；分享“题目 + 哈希 + 原始输出”，比只晒神图更有用。**

---

**Discover / 搜索关键词:** AI Agent Skill · Claude Code Skill · Codex CLI · MCP-compatible workflows · Prompt Engineering · Stochastic Entropy Injection · Cure Mode Collapse (research aspiration) · Divergent Thinking · 超级想法 · AI创意抽卡 · 随机哈希提示词 · 打破大模型同质化 · Agent技能
