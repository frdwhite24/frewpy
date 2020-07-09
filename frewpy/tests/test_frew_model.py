import os

import pytest

from test_config import TEST_DATA
from frewpy import FrewModel


@pytest.fixture
def frew_model():
    return FrewModel(os.path.join(TEST_DATA, 'test_model_1.json'))
