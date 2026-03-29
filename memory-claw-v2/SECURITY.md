# Security

This toolkit is intended to be safe to publish.

## Do not commit

- API keys
- auth tokens
- personal memory databases
- real user transcripts
- copied production `openclaw.json` files with secrets

## Expected runtime secrets

- `VOYAGE_API_KEY`
- any local OpenClaw provider auth already managed on the host

## Safe publishing rule

Only commit:

- templates
- schemas
- docs
- sanitized examples
- generic scripts

If you capture benchmark data from a real system, sanitize or aggregate it before publishing.
