import os
import json

import pytest

from test_config import TEST_DATA
from frewpy.models import Water


@pytest.fixture
def water_model():
    with open(os.path.join(TEST_DATA, "test_model_with_results.json")) as file:
        loaded_data = json.loads(file.read())
    return Water(loaded_data)


def test_get_water_pressures(water_model):
    water_pressure = water_model.get_water_pressures()
    assert len(list(water_pressure.keys())) == 11
    assert water_pressure[10]['SLS']['left'][9] == pytest.approx(2.207249)
    assert water_pressure[9]['SLS']['right'][-1] == pytest.approx(282.131010)
