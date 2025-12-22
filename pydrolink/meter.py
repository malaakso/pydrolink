"""WaterMeter abstraction representing a single meter tied to a Hydrolink account."""
from __future__ import annotations

from typing import Optional

from .client import HydrolinkClient


class WaterMeter:
    def __init__(self, *, client: HydrolinkClient, meter_id: int, code: Optional[str] = None, warm: bool = False, apartment_id: Optional[int] = None):
        self.client = client
        self.id = int(meter_id)
        self.code = code
        self.warm = bool(warm)
        self.apartment_id = apartment_id

    async def current_reading(self) -> Optional[dict]:
        readings = await self.client.get_current_readings()
        for r in readings:
            try:
                if int(r.get("meter_id")) == self.id:
                    return r
            except Exception:
                continue
        return None

    async def alarms(self) -> Optional[dict]:
        alarms = await self.client.get_alarms()
        for a in alarms:
            try:
                if int(a.get("meter_id")) == self.id:
                    return a
            except Exception:
                continue
        return None

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"<WaterMeter id={self.id} code={self.code} warm={self.warm}>"
