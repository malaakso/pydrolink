from pydrolink.meter import WaterMeter


def test_water_meter_repr_and_attrs():
    wm = WaterMeter(client=None, meter_id=165255, code="111", warm=True, apartment_id=81065)
    assert wm.id == 165255
    assert wm.code == "111"
    assert wm.warm is True
    assert "WaterMeter" in repr(wm)
