"""Parsing and normalization helpers for Hydrolink JSON responses."""
from typing import Any
from datetime import datetime


def to_bool(val: Any) -> bool:
    """Normalize boolean-like values from API to Python bool.

    Accepts: True/False, "t"/"f", "true"/"false", 1/0, and returns bool.
    """
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    s = str(val).strip().lower()
    return s in ("t", "true", "1", "yes")


def parse_price_str(s: Any) -> float | None:
    """Parse price strings that may use comma as decimal separator.

    Example: "8,51" -> 8.51
    Returns None if value is empty or cannot be parsed.
    """
    if s is None:
        return None
    try:
        ss = str(s).strip()
        ss = ss.replace(" ", "")
        if "," in ss and "." not in ss:
            ss = ss.replace(",", ".")
        return float(ss)
    except Exception:
        return None


def normalize_current_reading(r: dict) -> dict:
    """Normalize a single current reading dict in-place and return it."""
    out = dict(r)
    if "warm" in out:
        out["warm"] = to_bool(out.get("warm"))
    if "value" in out:
        try:
            out["value"] = int(out.get("value"))
        except (TypeError, ValueError):
            out["value"] = 0
    if "meter_id" in out:
        try:
            out["meter_id"] = int(out.get("meter_id"))
        except (TypeError, ValueError):
            out["meter_id"] = 0
    # Parse from format YYYY-MM-DD HH:MM:SS, if present to a datetime object
    if "created" in out:
        try:
            created_str = out.get("created")
            out["created"] = datetime.strptime(
                created_str, "%Y-%m-%d %H:%M:%S"
            )
        except (TypeError, ValueError):
            out["created"] = datetime.fromtimestamp(0)
    return out


def normalize_alarm(alarm: dict) -> dict:
    """Normalize a single alarm dict in-place and return it."""
    out = dict(alarm)
    """ Convert possible alarms to booleans
        "overflow": "false",
        "battery_change": "false",
        "removed": "false",
        "bwflow": "false",
        "waterloss": "false",
        "mag_fraud": "false",
        "waterloss_calculated": "false",
        "opt_fraud": "false",
    """
    for key in [
        "overflow",
        "battery_change",
        "removed",
        "bwflow",
        "waterloss",
        "mag_fraud",
        "waterloss_calculated",
        "opt_fraud",
    ]:
        if key in out:
            out[key] = to_bool(out.get(key))
    if "meter_id" in out:
        try:
            out["meter_id"] = int(out.get("meter_id"))
        except (TypeError, ValueError):
            out["meter_id"] = 0
    if "created" in out:
        try:
            created_str = out.get("created")
            out["created"] = datetime.strptime(
                created_str, "%Y-%m-%d %H:%M:%S"
            )
        except (TypeError, ValueError):
            out["created"] = datetime.fromtimestamp(0)
    return out
