# Required Tools

Install in this order.

## Core

```bash
# Node.js 18+
brew install node

# Python 3.10+
brew install python

# Go (for gopls)
brew install go

# Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

## GSD (get-shit-done-cc)

```bash
# Run from your AI project root
cd ~/Desktop/AI
npx get-shit-done-cc --claude --local
# GSD v1.29.0 confirmed working on this machine
```

## Context7

```bash
npm install -g ctx7
```

## uvx (for Serena MCP)

```bash
pip install uv
# After install, uvx available at ~/.local/bin/uvx
# or:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## codebase-memory-mcp (for Web2 MCP)

```bash
# Download binary from:
# https://github.com/shaneholloman/codebase-memory-mcp/releases
# Place at:
mkdir -p ~/.local/bin
mv codebase-memory-mcp ~/.local/bin/
chmod +x ~/.local/bin/codebase-memory-mcp
```

## LSP binaries (required for LSP plugins)

```bash
# TypeScript LSP
npm install -g typescript typescript-language-server

# Python LSP
npm install -g pyright

# Go LSP
go install golang.org/x/tools/gopls@latest

# Rust Analyzer
brew install rust-analyzer
# or: rustup component add rust-analyzer

# Flutter / Dart
brew install --cask flutter
# Verify: dart --version && flutter --version
```

## OpenClaw + Engram (optional — cross-session memory)

```bash
npm install -g openclaw
openclaw setup
openclaw plugins install @joshuaswarren/openclaw-engram
# Optional context engine:
openclaw plugins install @martian-engineering/lossless-claw
```

## Verify all

```bash
claude --version
node --version
python3 --version
go version
gopls version
typescript-language-server --version
pyright --version
uvx --version 2>/dev/null || ~/.local/bin/uvx --version
~/.local/bin/codebase-memory-mcp --version 2>/dev/null || echo "check binary"
```
