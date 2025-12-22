"""Async Hydrolink client using aiohttp.

Provides a small, resilient client that handles login token
and retries once on 401.
"""
from __future__ import annotations

from typing import Any, Optional

import aiohttp

from .parsers import normalize_current_reading, normalize_alarm


class AuthenticationError(Exception):
    """Raised when authentication with the Hydrolink API fails.

    Invalid credentials will trigger this exception.
    """


class HydrolinkClient:
    def __init__(
        self,
        username: str,
        password: str,
        *,
        base_url: str = "https://hydrolink.fi/api/v2",
        session: Optional[aiohttp.ClientSession] = None,
        timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=10),
    ):
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip("/")
        self._token: Optional[str] = None
        self._external_session = session is not None
        self._session = session
        self._timeout = timeout

    async def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        if self._session and not self._external_session:
            await self._session.close()

    async def login(self) -> str:
        session = await self._ensure_session()
        url = f"{self.base_url}/login"
        payload = {"username": self.username, "password": self.password}
        headers = {"Content-Type": "application/json"}
        async with session.post(
            url, json=payload, headers=headers, timeout=self._timeout
        ) as resp:
            if resp.status == 401:
                # Invalid credentials
                raise AuthenticationError("invalid username or password")
            resp.raise_for_status()
            data = await resp.json()
            token = data.get("token")
            self._token = token
            return token

    async def _post(
        self,
        path: str,
        payload: dict[str, Any] | None = None,
        retry: bool = True,
    ) -> Any:
        session = await self._ensure_session()
        payload = dict(payload or {})
        if self._token:
            payload.setdefault("token", self._token)
        else:
            await self.login()
            payload.setdefault("token", self._token)
        url = f"{self.base_url}/{path}"
        headers = {"Content-Type": "application/json"}
        async with session.post(
            url, json=payload, headers=headers, timeout=self._timeout
        ) as resp:
            if resp.status == 401 and retry:
                # stale token, try to re-login once
                try:
                    await self.login()
                except AuthenticationError:
                    # propagate so callers know credentials are invalid
                    raise
                return await self._post(path, payload, retry=False)
            resp.raise_for_status()
            return await resp.json(content_type="text/plain")

    async def get_apartment_info(self) -> dict:
        return await self._post("getResidentCompanyData", {})

    async def get_current_readings(self) -> list[dict]:
        raw = await self._post("current", {})
        if isinstance(raw, list):
            return [normalize_current_reading(r) for r in raw]
        return raw

    async def get_alarms(self) -> list[dict]:
        raw = await self._post("getAlarms", {})
        if isinstance(raw, list):
            return [normalize_alarm(r) for r in raw]
        return raw
