"""Service layer for Hydrolink water meters."""

from pydrolink.client import HydrolinkClient
from pydrolink.meter import WaterMeter, MeterReading, MeterAlarm


class WaterMeterService:
    def __init__(self, client: HydrolinkClient):
        self.client = client
        self.warm_water_price = 0.0
        self.cold_water_price = 0.0
        self._meters: list[WaterMeter] = []

    async def list_meters(self) -> list[WaterMeter]:
        if self._meters:
            return self._meters
        raw_info = await self.client.get_apartment_info()
        self.warm_water_price = raw_info.get("warmWaterPrice", 0.0)
        self.cold_water_price = raw_info.get("coldWaterPrice", 0.0)
        for meter in raw_info.get("meters", []):
            meter_id = meter.get("id")
            if meter_id is None:
                continue
            try:
                self._meters.append(
                    WaterMeter(
                        id=meter_id,
                        warm=meter.get("warm", False),
                        code=meter.get("code"),
                    )
                )
            except (TypeError, ValueError):
                continue
        return self._meters

    async def get_readings(self) -> dict[int, MeterReading]:
        raw_readings = await self.client.get_current_readings()
        out: dict[int, MeterReading] = {}
        for reading in raw_readings:
            meter_id = reading.get("meter_id")
            if meter_id is None:
                continue
            try:
                out[meter_id] = (
                    MeterReading(
                        id=int(meter_id),
                        value=reading.get("value"),
                        timestamp=reading.get("created")
                    )
                )
            except (TypeError, ValueError):
                continue
        return out

    async def get_alarms(self) -> dict[int, MeterAlarm]:
        raw_alarms = await self.client.get_alarms()
        out: dict[int, MeterAlarm] = {}
        for alarm in raw_alarms:
            meter_id = alarm.get("meter_id")
            if meter_id is None:
                continue
            try:
                alarm_flags = {
                    key: value
                    for key, value in alarm.items()
                    if key not in ("meter_id", "created")
                }
                out[meter_id] = (
                    MeterAlarm(
                        id=int(meter_id),
                        timestamp=alarm.get("created"),
                        alarms=alarm_flags
                    )
                )
            except (TypeError, ValueError):
                continue
        return out

    def get_warm_water_price(self) -> float:
        return self.warm_water_price

    def get_cold_water_price(self) -> float:
        return self.cold_water_price

    # Setters for prices, in case not set by company
    def set_warm_water_price(self, price: float) -> None:
        self.warm_water_price = price

    def set_cold_water_price(self, price: float) -> None:
        self.cold_water_price = price
