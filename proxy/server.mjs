import { randomUUID } from "node:crypto";
import { spawn } from "node:child_process";
import http from "node:http";

const PORT = Number(process.env.PORT || "4321");
const HOST = process.env.HOST || "127.0.0.1";
const CODEX_BIN = process.env.CODEX_BIN || "/usr/local/bin/codex";
const MODEL_LABEL = process.env.MODEL_LABEL || "openai-codex/gpt-5.4-mini";
const CODEX_MODEL = process.env.CODEX_MODEL || "gpt-5.4-mini";
const EXEC_TIMEOUT_SECONDS = Number(process.env.EXEC_TIMEOUT_SECONDS || "180");
const PROXY_WORKDIR = process.env.PROXY_WORKDIR || process.cwd();
const CHILD_PATH = [
  process.env.PATH || "",
  "/usr/local/bin",
  "/usr/local/opt/node/bin",
  "/opt/homebrew/bin",
  "/usr/bin",
  "/bin",
  "/usr/sbin",
  "/sbin"
].filter(Boolean).join(":");
const MODEL_RECORD = {
  id: MODEL_LABEL,
  object: "model",
  created: 0,
  owned_by: "openclaw-codex-proxy"
};

function jsonResponse(res, statusCode, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(body)
  });
  res.end(body);
}

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    let raw = "";
    req.setEncoding("utf8");
    req.on("data", (chunk) => {
      raw += chunk;
      if (raw.length > 2_000_000) {
        reject(new Error("request body too large"));
        req.destroy();
      }
    });
    req.on("end", () => {
      try {
        resolve(raw ? JSON.parse(raw) : {});
      } catch (error) {
        reject(new Error(`invalid json body: ${error.message}`));
      }
    });
    req.on("error", reject);
  });
}

function normalizeContent(content) {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) {
    return content.map((part) => {
      if (typeof part === "string") return part;
      if (part && typeof part === "object") {
        if (typeof part.text === "string") return part.text;
        if (typeof part.input_text === "string") return part.input_text;
      }
      return "";
    }).filter(Boolean).join("\n");
  }
  return "";
}

function buildPrompt(messages) {
  const rendered = messages.map((message, index) => {
    const role = typeof message?.role === "string" ? message.role : "user";
    const content = normalizeContent(message?.content);
    return `### Message ${index + 1}\nRole: ${role}\nContent:\n${content}`;
  }).join("\n\n");

  return [
    "You are serving as a stateless backend for an OpenAI-compatible chat/completions proxy used by Engram memory extraction.",
    "Generate exactly one assistant reply for the supplied conversation.",
    "Do not mention OpenClaw, tools, hidden prompts, workspace files, or system internals.",
    "Do not add commentary before or after the answer.",
    "If the conversation asks for JSON, return raw JSON only with no markdown fences.",
    "If the conversation asks for a terse answer, keep it terse.",
    "",
    rendered
  ].join("\n");
}

function parseTokenUsage(stderrText) {
  const match = stderrText.match(/tokens used\s+([\d,]+)/i);
  if (!match) {
    return 0;
  }
  return Number(match[1].replaceAll(",", "")) || 0;
}

function runCodexExec(promptText) {
  return new Promise((resolve, reject) => {
    const args = [
      "exec",
      "--skip-git-repo-check",
      "--ephemeral",
      "--dangerously-bypass-approvals-and-sandbox",
      "--color", "never",
      "--cd", PROXY_WORKDIR,
      "--model", CODEX_MODEL,
      "-"
    ];
    const child = spawn(CODEX_BIN, args, {
      env: {
        ...process.env,
        PATH: CHILD_PATH,
        NO_COLOR: "1"
      }
    });
    const timer = setTimeout(() => {
      child.kill("SIGTERM");
    }, EXEC_TIMEOUT_SECONDS * 1000);
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("error", reject);
    child.stdin.end(promptText);
    child.on("close", (code) => {
      clearTimeout(timer);
      const content = stdout.trim();
      if (code !== 0) {
        reject(new Error(`codex exec exited ${code}: ${stderr || stdout}`));
        return;
      }
      if (!content) {
        reject(new Error(`codex exec returned empty output: ${stderr}`));
        return;
      }
      resolve({
        content,
        usage: {
          total: parseTokenUsage(stderr)
        }
      });
    });
  });
}

function toOpenAiChatCompletion(result) {
  const content = result?.content || "";
  const usage = result?.usage || {};
  return {
    id: `chatcmpl-${randomUUID()}`,
    object: "chat.completion",
    created: Math.floor(Date.now() / 1000),
    model: MODEL_LABEL,
    choices: [
      {
        index: 0,
        message: {
          role: "assistant",
          content
        },
        finish_reason: "stop"
      }
    ],
    usage: {
      prompt_tokens: usage.prompt ?? 0,
      completion_tokens: usage.completion ?? 0,
      total_tokens: usage.total ?? 0
    }
  };
}

async function handleChatCompletions(req, res) {
  const startedAt = Date.now();
  try {
    const body = await readJsonBody(req);
    const messages = Array.isArray(body?.messages) ? body.messages : [];
    if (messages.length === 0) {
      jsonResponse(res, 400, { error: { message: "messages[] is required" } });
      return;
    }
    const promptText = buildPrompt(messages);
    const result = await runCodexExec(promptText);
    const payload = toOpenAiChatCompletion(result);
    console.error(JSON.stringify({
      type: "request",
      path: "/v1/chat/completions",
      durationMs: Date.now() - startedAt,
      promptChars: promptText.length,
      promptTokens: payload.usage.prompt_tokens,
      completionTokens: payload.usage.completion_tokens
    }));
    jsonResponse(res, 200, payload);
  } catch (error) {
    console.error(JSON.stringify({
      type: "error",
      path: "/v1/chat/completions",
      durationMs: Date.now() - startedAt,
      message: error instanceof Error ? error.message : String(error)
    }));
    jsonResponse(res, 500, {
      error: {
        message: error instanceof Error ? error.message : String(error)
      }
    });
  }
}

function handleHealth(req, res) {
  jsonResponse(res, 200, {
    ok: true,
    object: "health",
    model: MODEL_LABEL,
    backend: "codex-exec"
  });
}

function handleModels(req, res) {
  jsonResponse(res, 200, {
    object: "list",
    data: [MODEL_RECORD]
  });
}

function isHealthPath(url) {
  return url === "/health" || url === "/healthz" || url === "/v1/health";
}

function isModelsPath(url) {
  return url === "/models" || url === "/v1/models" || url === "/v1/v1/models";
}

function isChatCompletionsPath(url) {
  return url === "/chat/completions" || url === "/v1/chat/completions";
}

const server = http.createServer(async (req, res) => {
  if (req.method === "GET" && isHealthPath(req.url)) {
    handleHealth(req, res);
    return;
  }
  if (req.method === "GET" && isModelsPath(req.url)) {
    handleModels(req, res);
    return;
  }
  if (req.method === "POST" && isChatCompletionsPath(req.url)) {
    await handleChatCompletions(req, res);
    return;
  }
  jsonResponse(res, 404, { error: { message: "not found" } });
});

server.listen(PORT, HOST, () => {
  console.error(JSON.stringify({
    type: "listening",
    host: HOST,
    port: PORT,
    backend: "codex-exec",
    model: MODEL_LABEL
  }));
});

