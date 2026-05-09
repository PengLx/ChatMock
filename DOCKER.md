# Docker Deployment

## Quick Start
1) Setup env:
   cp .env.example .env

   If you built the image locally, keep `CHATMOCK_IMAGE=chatmock:gpt-5.5`.
   If you are pulling a published image, set `CHATMOCK_IMAGE` to that tag.

2) Login:
   docker compose run --rm --service-ports chatmock-login login

   - The command prints an auth URL, copy paste it into your browser.
   - If your browser cannot reach the container's localhost callback, copy the full redirect URL from the browser address bar and paste it back into the terminal when prompted.
   - Server should stop automatically once it receives the tokens and they are saved.

3) Start the server:
   docker compose up -d chatmock

4) Free to use it in whichever chat app you like!

## Configuration
Set options in `.env` or pass environment variables:
- `PORT`: Container listening port (default 8000)
- `LOGIN_PORT`: Host port for the OAuth callback (default 1455)
- `CHATMOCK_IMAGE`: image tag to run (default `chatmock:gpt-5.5` in `.env.example`)
- `CHATGPT_LOCAL_HOME`: Container auth directory (default `/data`)
- `CHATMOCK_AUTH_SOURCE`: Named volume or host directory mounted at `/data` (default `chatmock_data`)
- `CHATMOCK_PROMPT_FILE`: Host prompt file mounted into the container (default `./prompt.md`)
- `VERBOSE`: `true|false` to enable request/stream logs
- `VERBOSE_OBFUSCATION`: `true|false` to include raw SSE/obfuscation logs
- `CHATGPT_LOCAL_REASONING_EFFORT`: none|minimal|low|medium|high|xhigh
- `CHATGPT_LOCAL_REASONING_SUMMARY`: auto|concise|detailed|none
- `CHATGPT_LOCAL_REASONING_COMPAT`: legacy|o3|think-tags|current
- `CHATGPT_LOCAL_FAST_MODE`: `true|false` to enable fast mode by default for supported models
- `CHATGPT_LOCAL_CLIENT_ID`: OAuth client id override (rarely needed)
- `CHATGPT_LOCAL_EXPOSE_REASONING_MODELS`: `true|false` to add reasoning model variants to `/v1/models`
- `CHATGPT_LOCAL_ENABLE_WEB_SEARCH`: `true|false` to enable default web search tool
- `CHATGPT_LOCAL_DEBUG_MODEL`: force all requests to a specific upstream model, for example `gpt-5.5`

## Auth Options

By default, Docker login stores tokens in the `chatmock_data` named volume:

```
CHATMOCK_AUTH_SOURCE=chatmock_data
CHATGPT_LOCAL_HOME=/data
```

To reuse an existing server-side Codex or ChatMock login, point `CHATMOCK_AUTH_SOURCE` at the directory that contains `auth.json`:

```
CHATMOCK_AUTH_SOURCE=/home/you/.codex
CHATGPT_LOCAL_HOME=/data
```

The host directory is mounted to `/data`, so ChatMock reads `/data/auth.json` in the container.

## Logs
Set `VERBOSE=true` to include extra logging for troubleshooting upstream or chat app requests. Please include and use these logs when submitting bug reports.

## Test

```
curl -s http://localhost:8000/v1/chat/completions \
   -H 'Content-Type: application/json' \
   -d '{"model":"gpt-5.5","messages":[{"role":"user","content":"Hello world!"}]}' | jq .
```
