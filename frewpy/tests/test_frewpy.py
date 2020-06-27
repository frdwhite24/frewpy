import os

import pytest

from test_config import TEST_DATA
from frewpy import FrewModel
from frewpy.models.exceptions import (
    FrewpyFileExtensionNotRecognised,
    FrewError,
    NodeError,
)


@pytest.fixture
def model():
    model_name = 'test_model_1.json'
    return FrewModel(os.path.join(TEST_DATA, model_name))


def test_check_path_exists(model):
    assert model.path_exists


def test_check_path_does_not_exist():
    model_name = 'test_model_1_ does_not_exists.json'
    with pytest.raises(FileNotFoundError):
        model = FrewModel(os.path.join(TEST_DATA, model_name))


def test_check_extension():
    model_name = 'wrong_file_path.txt'
    with pytest.raises(FrewpyFileExtensionNotRecognised):
        model = FrewModel(os.path.join(TEST_DATA, model_name))


def test_num_nodes(model):
    assert model.num_nodes == 68


def test_first_material(model):
    materials = model.get_materials()
    assert materials[0] == 'Made Ground'


def test_fifth_material(model):
    materials = model.get_materials()
    assert materials[4] == 'LC A - drained'


def test_no_materials(model):
    model_name = 'empty_model.json'
    model = FrewModel(os.path.join(TEST_DATA, model_name))
    with pytest.raises(FrewError):
        model.get_materials()


def test_no_material_properties(model):
    model_name = 'empty_model.json'
    model = FrewModel(os.path.join(TEST_DATA, model_name))
    with pytest.raises(FrewError):
        model.get_material_properties()
