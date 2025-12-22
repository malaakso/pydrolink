# Copilot instructions for pydrolink

This file gives concise, actionable guidance for AI coding agents working on pydrolink.

- Project summary: small Python library that interfaces with the Hydrolink HTTP RPC API (see [API.md](API.md)).
- Language & tooling: Python 3.10+, dependency management with Poetry (`pyproject.toml`). Key runtime dependency: `aiohttp`.

- Big picture:
  - The code is a client library that constructs JSON POST payloads and parses JSON responses from Hydrolink endpoints.
  - Authentication: the API expects the login `token` included inside every POST JSON payload (login via `/api/v2/login`). See [API.md](API.md#login) for example payloads.
  - Responses are inconsistent: booleans may appear as `"t"`/`"f"`, `"true"`/`"false"` strings, or real booleans; numeric prices use comma decimal separators; some IDs appear as strings in some endpoints and integers in others. Handle these consistently in parsing.

- Important data patterns to handle (use examples from [API.md](API.md)):
  - Login payload: `{"username": "myuser", "password": "mypass"}` → response `{"token": "..."}`
  - Current readings: `"warm": "t" | "f"`, `"value"` is liters as string, `"meter_id"` sometimes string. Normalize types (bool, int, int/float) early.
  - Prices: `"warmWaterPrice": "8,51"` — parse comma as decimal separator.
  - Historical timestamps: sometimes provided as UNIX milliseconds. Expect large integers.

- Conventions & patterns used in this repo (follow these precisely):
  - Normalize incoming JSON immediately: convert "t"/"f" and "true"/"false" to booleans, strip and convert numeric strings to ints/floats, and parse comma decimals to floats.
  - Keep parsing logic separate from transport (HTTP) code so callers can reuse parsers for cached or test data.
  - Use `aiohttp` for HTTP calls and async API surface in the client library (project uses `aiohttp` in `pyproject.toml`).

- Build / dev workflow (commands likely to work locally):
  - Install dependencies: `poetry install` (uses [pyproject.toml](pyproject.toml)).
  - Run quick interactive test: open Python REPL with the project environment and import the client module to exercise API calls.
  - There are no project-specific test commands in the repo; prefer creating small async integration tests that mock HTTP with `aiohttp` test utilities.

- Integration & external dependencies:
  - External: Hydrolink API over HTTPS (hosted at `https://hydrolink.fi/api/v2/*`). All network behaviour must be written defensively (timeouts, retries, 401 handling → re-login).
  - Token lifetime appears long but server can return 401; client should transparently re-login and retry the request.

- Files to reference when changing behavior:
  - README: [README.md](README.md) — project purpose.
  - API surface and examples: [API.md](API.md) — canonical examples to match request/response handling.
  - Dependency list: [pyproject.toml](pyproject.toml).

- Suggested first edits an agent may be asked to do (examples):
  - Add a small helper `normalize_response()` that converts the three boolean formats to Python `bool` and normalizes numeric fields; include unit tests that feed examples from [API.md](API.md).
  - Add parsing utilities for comma-decimal prices (e.g., `parse_price_str("8,51") -> 8.51`).
  - Implement resilient HTTP helper that retries once on 401 after refreshing token.

- When uncertain, prefer small, well-scoped changes (one helper or parser per PR) and reference the exact API examples in [API.md](API.md).

- If something here is unclear or you want more detail about a specific directory or module, tell me which file to inspect next.
