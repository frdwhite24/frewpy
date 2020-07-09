import os

import pytest

from test_config import TEST_DATA
from frewpy import FrewModel
from frewpy.models.exceptions import FrewError


@pytest.fixture
def frew_model():
    return FrewModel(os.path.join(TEST_DATA, "test_model_1.json"))


def test_get_request_not_string(frew_model):
    with pytest.raises(FrewError):
        frew_model.get(123)


def test_get_titles(frew_model):
    titles = frew_model.get("titles")
    assert isinstance(titles, dict)
    assert titles["JobNumber"] == "261026"
    assert titles["JobTitle"] == "Elizabeth House "
    assert titles["Initials"] == "FW"


def test_get_file_history(frew_model):
    file_history = frew_model.get("file history")
    assert len(file_history) == 4
    assert file_history[0]["Time"] == "08:01"
    assert file_history[2]["Date"] == "10-Jun-2020"


def test_get_file_version(frew_model):
    assert frew_model.get("file version") == "19.4.0.23"


def test_get_frew_version(frew_model):
    assert frew_model.get("frew version") == "19.4"


def test_get_num_stages(frew_model):
    assert frew_model.get("num stages") == 11


def test_get_stage_names(frew_model):
    assert frew_model.get("stage names")[0] == "Initial condition"
    assert frew_model.get("stage names")[3] == "  Excavate to B02 (-6.55mOD)"
    assert (
        frew_model.get("stage names")[-1]
        == " Long-term (relaxation and creep)"
    )


def test_get_num_nodes(frew_model):
    assert frew_model.get("num nodes") == 68


def test_get_wrong_entry(frew_model):
    with pytest.raises(FrewError):
        frew_model.get("hello")
