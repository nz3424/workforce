# Daily Learning Log

> Running log of things Nick learned, one section per day.
> Append-only — newest section goes at the bottom. Never edit past entries.
> Captured via manual "Log: ..." entries or the end-of-day recap pass.
> See `agent.md` for capture rules.

---

## 2026-07-17
- [Transformers/Backprop] Residual connections act as a gradient "floor" via the chain rule expanding into a sum over 2^L skip/pass-through paths — not a literal `+1` you can trace back — and that floor only protects gradient flow *between* blocks, never a block's own internal weights.
- [Transformers/Backprop] The residual `+1` guards against vanishing gradients but not exploding ones (since `1+f' > f'` for `f'>0`) — normalization, init, and clipping do the exploding-gradient job separately.
- [Transformers/FFN] The FFN block works as a per-token key-value lookup — `W1` rows are detectors, `W2` columns are the associated values — and confirmed this mapping against the real `llm-training/src` code (GELU, 4x `d_ff`, pre-norm structure).
- [Transformers/Attention] Softmax's Jacobian is symmetric (it's the Hessian of log-sum-exp), and a confident/peaked softmax has a near-dead local gradient — the actual mechanistic reason `1/√d_k` scaling matters for training, not just numerics.
- [Process] Set a personal teaching preference going forward: work through concepts with real worked/numerical examples before comprehension checks (not intro-then-quiz), and capture clarifications into each track's README Notes section as they come up, not just leave them in chat.
- [Workforce/Automation] Designed and built the `/recap` Learning Log agent (manual capture, daily recap, retrieval modes) as a new Operations Team agent, then added `extract_transcripts.py` so daily recap can pull today's learnings straight from raw session transcripts across every project, not just `session-log.md`.
- [llm-training] Distinguished parameters (persist across steps, updated by `optimizer.step()`) from activations (recomputed fresh every forward pass, discarded) — `x`, `Q`, `K`, `V` never "get updated" themselves, only the weights that produce them do.
- [llm-training] Built a full parameter inventory for the actual `TinyTransformer` (~1.08M params: embeddings, Q/K/V/out projections, LayerNorms, FFN linears, head), and clarified attention's output isn't logits — logits only exist after the final head projection.
- [llm-training] Clarified `out_proj`'s semantic role: recombining separate attention heads' independent findings into one unified vector (vs. Q/K/V's job of building the attention mechanism itself).
- [Transformers] Worked through why Q/K/V must be separate matrices — tying `W_Q=W_K` forces symmetric attention (breaks asymmetric cases like pronoun→antecedent); tying `V=K` creates a representational bottleneck (K's job is "be matchable," V's job is "carry content").
- [Transformers] Traced the full forward-pass shape pipeline end to end (token IDs → embeddings → per-head attention → logits), including why causal masking is a per-row, not uniform, lower-triangular mask.
- [Transformers] Learned RoPE's mechanism (rotates Q/K by position-dependent angles so only relative position survives the dot product) and its payoff over learned absolute embeddings — no hard context-length ceiling, graceful degradation instead of a crash past position 256.
