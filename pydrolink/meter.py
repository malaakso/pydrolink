"""Domain models for Hydrolink water meters."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
from datetime import datetime


@dataclass(slots=True)
class WaterMeter:
    id: int
    warm: bool = False
    code: Optional[str] = None


@dataclass(slots=True)
class MeterReading:
    id: int
    value: int | None = None
    timestamp: datetime | None = None


@dataclass(slots=True)
class MeterAlarm:
    id: int
    timestamp: datetime | None = None
    alarms: dict[str, Any] | None = None
