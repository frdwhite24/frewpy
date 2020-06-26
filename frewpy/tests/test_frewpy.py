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


def test_titles_job_number(model):
    assert model.titles['JobNumber'] == '261026'


def test_titles_job_title(model):
    assert model.titles['JobTitle'] == 'Elizabeth House '


def test_titles_initials(model):
    assert model.titles['Initials'] == 'FW'


def test_file_history_first(model):
    assert model.file_history[0] == {
        "Date": "10-Jun-2020",
        "Time": "08:01",
        "Mode": "Edit",
        "User": "Fred.White",
        "Comments": "New"
    }


def test_file_history_third(model):
    assert model.file_history[2] == {
        "Date": "10-Jun-2020",
        "Time": "09:06",
        "Mode": "Edit",
        "User": "Fred.White",
        "Comments": "Open"
    }


def test_file_version(model):
    assert model.file_version == '19.4.0.23'


def test_model_version(model):
    assert model.version == '19.4'


def test_num_stages(model):
    assert model.num_stages == 11


def test_second_stage_name(model):
    assert model.stage_names[1] == ' Install wall (900mm @ 1300mm C/C)'


def test_fifth_stage_name(model):
    assert model.stage_names[4] == (
        ' Cast B02 floor slab (350mm thk @ -6.375mOD)'
    )


def test_ninth_stage_name(model):
    assert model.stage_names[8] == (
        '  Cast B03 floor slab (2000mm thk @ -12.7mOD) - prop'
    )


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
