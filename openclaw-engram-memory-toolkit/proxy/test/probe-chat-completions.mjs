const baseUrl = process.env.PROXY_BASE_URL || "http://127.0.0.1:4321";

const response = await fetch(`${baseUrl}/v1/chat/completions`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    messages: [
      {
        role: "system",
        content: "Return the exact text requested by the user."
      },
      {
        role: "user",
        content: "Reply with exactly: pong"
      }
    ]
  })
});

const body = await response.text();
if (!response.ok) {
  console.error(body);
  process.exit(1);
}

const parsed = JSON.parse(body);
const content = parsed?.choices?.[0]?.message?.content?.trim();
if (content !== "pong") {
  console.error(`unexpected content: ${JSON.stringify(content)}`);
  process.exit(1);
}

console.log("probe ok");
