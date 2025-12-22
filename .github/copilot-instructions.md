# Copilot instructions for pydrolink

This file gives concise, actionable guidance for AI coding agents working on pydrolink. Follow the repo conventions exactly — small, focused changes are preferred.

- Project snapshot: a small async Python client for the Hydrolink HTTP RPC API. Key files:
  - `pydrolink/client.py`: transport layer using `aiohttp`, responsible for POST requests and token management.
  - `pydrolink/parsers.py`: normalization and parsing utilities (convert booleans, parse comma decimals, coerce numeric strings).
  - `pydrolink/meter.py`: domain models and higher-level helpers wrapping parsed data.
  - `pydrolink/cli.py`: small CLI wrapper for manual calls / debugging.

- Key conventions and patterns (must follow):
  - Always normalize API JSON as close to the boundary as possible: convert `"t"`/`"f"` and `"true"`/`"false"` → `bool`; numeric strings → `int`/`float`; prices with commas (e.g. `"8,51"`) → `float`.
  - Keep parsing separate from HTTP transport. Parsers are testable pure functions in `pydrolink/parsers.py` and should not perform network I/O.
  - Network code is async and uses `aiohttp`. Use explicit timeouts, handle 401 by refreshing token, then retry the failed request once.

- Data quirks to watch for (examples from API.md):
  - Login: send `{"username":..., "password":...}` → response contains `{"token": "..."}`; token is required inside every POST JSON payload.
  - Readings: fields like `"warm"` may be `"t"`/`"f"` or boolean; `"value"` and `"meter_id"` are sometimes strings.
  - Prices: `"warmWaterPrice": "8,51"` uses comma decimal separator.
  - Timestamps: sometimes UNIX milliseconds (large ints).

- Tests & developer workflow:
  - Use Poetry: `poetry install` to set up the environment.
  - Run tests with `poetry run pytest` (tests live in `tests/` — `test_parsers.py` and `test_meter.py`).
  - For network-dependent tests, mock `aiohttp` or use `aiohttp` test utilities — avoid real API calls in CI.

- Editing and PR guidance for agents:
  - Make minimal, focused changes. Prefer adding a small helper (e.g. `parse_price_str`, `normalize_response`) and matching unit tests in `tests/`.
  - When modifying `client.py`, preserve async semantics and token-retry behavior; when changing parsing, keep transport untouched and add tests.
  - Examples of low-level helpers to add: `parse_price_str("8,51") -> 8.51`, `coerce_bool(x) -> bool`, `coerce_int(x) -> int | None`.

- Integration points & external dependencies:
  - External API: https://hydrolink.fi/api/v2/* (HTTPS). Code must assume intermittent 401s and inconsistent typing.
  - Runtime dependency: `aiohttp` (declared in `pyproject.toml`).

- When in doubt, inspect these files first:
  - [pydrolink/client.py](pydrolink/client.py) — transport and token handling.
  - [pydrolink/parsers.py](pydrolink/parsers.py) — canonical normalization patterns.
  - [API.md](API.md) — canonical request/response examples to mirror in tests.

If something here is unclear or you want more detail about a specific module, tell me which file to inspect next.
