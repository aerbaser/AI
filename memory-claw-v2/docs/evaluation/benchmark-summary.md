# Benchmark Summary

This summary publishes the high-level findings from the memory comparison work without shipping private corpora.

## Full-turn benchmark snapshot

| Candidate | Avg Answer Quality | Avg Full-Turn Latency | Avg Answer Tokens | Reading |
|---|---:|---:|---:|---|
| `baseline-none` | `0.0` | `2945.33 ms` | `2250.0` | Honest floor with no retrieval |
| `lcm-like` | `0.1111` | `4626.5 ms` | `29271.67` | Live corpus contains facts, but context is noisy |
| `current-clean` | `0.1945` | `90875.5 ms` | `28004.67` | Cleaned current architecture can answer well, but retrieval is too slow and bloated |
| `memos-local` | `0.0555` | `4165.33 ms` | `13457.67` | Operationally simple, weaker quality |
| `demerzel-faithful-linux` | `0.1945` | `21007.0 ms` | `3008.17` | Strong answer quality, unacceptable runtime spikes |
| `engram-native-linux` | `0.1389` | `8801.67 ms` | `12084.0` | Strongest Linux-native replacement track, but extraction cost still needs work |

## Main conclusions

- `baseline-none` proves retrieval matters.
- `current-clean` proves the current architecture can still answer well if the corpus is cleaned.
- `Engram` is the strongest Linux-native replacement direction today.
- `Demerzel` still teaches useful policy ideas, but not a good Linux runtime default.
- `graph-memory` remains an R&D track with maturation potential, not the default product runtime.

## Product decision

The default public stack in `memory-claw-v2` is:

- `LCM` for session continuity
- `Engram` for primary long-term memory
- `QMD` for curated docs/shared-memory retrieval
- automatic ingestion instead of agent-only note taking

That choice balances quality, portability, and maintainability better than the alternatives tested so far.
