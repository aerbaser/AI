# AI

Публичный репозиторий с наборами инфраструктуры и тулкитами для агентных систем.

Сейчас внутри:

- `openclaw-engram-memory-toolkit/`
  Готовый toolkit для раскатки стека `OpenClaw + Engram + QMD + Voyager + Codex proxy`.

## Быстрый старт

```bash
git clone https://github.com/aerbaser/AI.git
cd AI/openclaw-engram-memory-toolkit

export VOYAGE_API_KEY="your-voyage-key"
export CODEX_MODEL="gpt-5.4-mini"

./install/bootstrap.sh
./install/verify.sh
```

Основная документация лежит в:

- [openclaw-engram-memory-toolkit/README.md](openclaw-engram-memory-toolkit/README.md)
- [openclaw-engram-memory-toolkit/docs/install-macos.md](openclaw-engram-memory-toolkit/docs/install-macos.md)
- [openclaw-engram-memory-toolkit/docs/llm-recommendations.md](openclaw-engram-memory-toolkit/docs/llm-recommendations.md)

