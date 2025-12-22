from pydrolink.parsers import (
    normalize_current_reading,
    normalize_alarm,
    parse_price_str,
    to_bool,
)


def test_parse_price_str():
    assert parse_price_str("8,51") == 8.51
    assert parse_price_str(" 1 234,50 ") == 1234.5
    assert parse_price_str(None) is None


def test_to_bool():
    assert to_bool("t") is True
    assert to_bool("f") is False
    assert to_bool(True) is True
    assert to_bool("true") is True
    assert to_bool("0") is False


def test_normalize_current_reading():
    raw = {
        "warm": "t",
        "code": "111",
        "meter_id": "165255",
        "value": "175518",
        "created": "2025-01-30 16:13:00",
        "secondary_address": "03118470"
    }
    n = normalize_current_reading(raw)
    assert isinstance(n["value"], int)
    assert n["warm"] is True
    assert isinstance(n["meter_id"], int)
    assert n["created"].year == 2025
    assert n["created"].month == 1
    assert n["created"].day == 30
    assert n["created"].hour == 16
    assert n["created"].minute == 13
    assert n["created"].second == 0
    assert n["code"] == "111"
    assert n["secondary_address"] == "03118470"


def test_normalize_alarm():
    raw = {
        "overflow": "false",
        "battery_change": "false",
        "removed": "false",
        "bwflow": "false",
        "waterloss": "false",
        "mag_fraud": "false",
        "meter_id": "165255",
        "waterloss_calculated": "false",
        "opt_fraud": "false",
        "created": "0"
    }
    n = normalize_alarm(raw)
    assert isinstance(n["meter_id"], int)
    assert n["overflow"] is False
    assert n["battery_change"] is False
    assert n["removed"] is False
    assert n["bwflow"] is False
    assert n["waterloss"] is False
    assert n["mag_fraud"] is False
    assert n["waterloss_calculated"] is False
    assert n["opt_fraud"] is False
    assert n["created"].timestamp() == 0
