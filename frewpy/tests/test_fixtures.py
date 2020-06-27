import os
import json

import pytest

from test_config import TEST_DATA
from frewpy import FrewModel


@pytest.fixture
def json_data():
    with open(os.path.join(TEST_DATA, 'test_model_1.json')) as file:
        return json.loads(file.read())


@pytest.fixture
def model():
    return FrewModel(os.path.join(TEST_DATA, 'test_model_1.json'))


@pytest.fixture
def empty_model():
    return FrewModel(os.path.join(TEST_DATA, 'empty_model.json'))
