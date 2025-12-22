"""Parsing and normalization helpers for Hydrolink JSON responses."""
from typing import Any

def to_bool(val: Any) -> bool:
    """Normalize boolean-like values from API to Python bool.

    Accepts: True/False, "t"/"f", "true"/"false", numeric 1/0, and returns bool.
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
            out["value"] = int(str(out.get("value")).strip())
        except Exception:
            try:
                out["value"] = float(str(out.get("value")).replace(",", "."))
            except Exception:
                out["value"] = out.get("value")
    if "meter_id" in out:
        try:
            out["meter_id"] = int(out.get("meter_id"))
        except Exception:
            out["meter_id"] = out.get("meter_id")
    return out
