import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, Mock

from pydrolink.client import HydrolinkClient
from pydrolink.meter import MeterAlarm, MeterReading, WaterMeter
from pydrolink.service import WaterMeterService


def _build_client_mock() -> Mock:
    client = Mock(spec=HydrolinkClient)
    client.get_apartment_info = AsyncMock()
    client.get_current_readings = AsyncMock()
    client.get_alarms = AsyncMock()
    return client


def test_service_list_meters_populates_cache_and_prices():
    async def run() -> None:
        client = _build_client_mock()
        client.get_apartment_info.return_value = {
            "warmWaterPrice": 8.51,
            "coldWaterPrice": 3.12,
            "meters": [
                {"id": 165255, "warm": True, "code": "111"},
                {"id": 165256, "warm": False, "code": "112"},
                {"id": None, "warm": False, "code": "bad"},
            ],
        }

        service = WaterMeterService(client)
        meters = await service.list_meters()
        meters_cached = await service.list_meters()

        assert meters == [
            WaterMeter(id=165255, warm=True, code="111"),
            WaterMeter(id=165256, warm=False, code="112"),
        ]
        assert meters_cached is meters
        assert service.warm_water_price == 8.51
        assert service.cold_water_price == 3.12
        client.get_apartment_info.assert_awaited_once()

    asyncio.run(run())


def test_service_get_readings():
    async def run() -> None:
        client = _build_client_mock()
        client.get_current_readings.return_value = [
            {
                "meter_id": 165255,
                "value": 175518,
                "created": datetime(2025, 1, 30, 16, 13, 0),
            },
            {
                "meter_id": 165256,
                "value": 80,
                "created": datetime(2025, 1, 30, 17, 0, 0),
            },
            {"meter_id": None, "value": 10, "created": datetime(2025, 1, 1)},
        ]

        service = WaterMeterService(client)

        all_readings = await service.get_readings()

        assert all_readings == {
            165255: MeterReading(
                id=165255,
                value=175518,
                timestamp=datetime(2025, 1, 30, 16, 13, 0),
            ),
            165256: MeterReading(
                id=165256,
                value=80,
                timestamp=datetime(2025, 1, 30, 17, 0, 0),
            ),
        }

    asyncio.run(run())


def test_service_get_alarms():
    async def run() -> None:
        client = _build_client_mock()
        client.get_alarms.return_value = [
            {
                "meter_id": 165255,
                "created": datetime(2025, 1, 30, 16, 13, 21),
                "overflow": True,
                "battery_change": False,
            },
            {
                "meter_id": 165256,
                "created": datetime(2025, 1, 30, 16, 14, 0),
                "overflow": False,
            },
            {"meter_id": None, "created": datetime(2025, 1, 1)},
        ]

        service = WaterMeterService(client)

        alarms = await service.get_alarms()

        assert alarms == {
            165255: MeterAlarm(
                id=165255,
                timestamp=datetime(2025, 1, 30, 16, 13, 21),
                alarms={"overflow": True, "battery_change": False},
            ),
            165256: MeterAlarm(
                id=165256,
                timestamp=datetime(2025, 1, 30, 16, 14, 0),
                alarms={"overflow": False},
            ),
        }

    asyncio.run(run())


def test_water_price_getters_default_to_zero():
    client = _build_client_mock()
    service = WaterMeterService(client)

    assert service.get_warm_water_price() == 0.0
    assert service.get_cold_water_price() == 0.0


def test_water_price_setters_and_getters_roundtrip():
    client = _build_client_mock()
    service = WaterMeterService(client)

    service.set_warm_water_price(8.51)
    service.set_cold_water_price(3.12)

    assert service.get_warm_water_price() == 8.51
    assert service.get_cold_water_price() == 3.12
