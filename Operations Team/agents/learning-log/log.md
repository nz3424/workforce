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
