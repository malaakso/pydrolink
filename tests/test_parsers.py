from pydrolink.parsers import parse_price_str, to_bool, normalize_current_reading


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
    raw = {"warm": "t", "meter_id": "165255", "value": "175518"}
    n = normalize_current_reading(raw)
    assert isinstance(n["value"], int)
    assert n["warm"] is True
    assert isinstance(n["meter_id"], int)
