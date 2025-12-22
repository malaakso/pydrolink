from pydrolink.meter import (
    MeterAlarm,
    MeterReading,
    WaterMeter
)

import datetime


def test_meter_dataclasses_attrs():
    meter = WaterMeter(id=165255, code="111", warm=True)
    reading = MeterReading(id=165255, value=175518, timestamp=datetime.datetime(2025, 1, 30, 16, 13, 0))
    alarm = MeterAlarm(id=165255, timestamp=datetime.datetime(2025, 1, 30, 16, 13, 21), alarms={"alarm": True})

    assert meter.id == 165255
    assert meter.code == "111"
    assert meter.warm is True
    assert reading.value == 175518
    assert reading.timestamp == datetime.datetime(2025, 1, 30, 16, 13, 0)
    assert alarm.timestamp == datetime.datetime(2025, 1, 30, 16, 13, 21)
    assert alarm.alarms == {"alarm": True}

