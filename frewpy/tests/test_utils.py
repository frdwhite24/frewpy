import os

import pytest

from test_config import TEST_DATA
from test_fixtures import json_data, json_data_with_results
from frewpy.utils import (
    _check_frew_path,
    check_json_path,
    load_data,
    model_to_json,
    get_titles,
    get_file_history,
    get_file_version,
    get_frew_version,
    get_num_stages,
    get_stage_names,
    get_num_nodes,
    clear_results,
    get_num_design_cases,
    get_design_case_names,
    check_results_present,
)
from frewpy.models.exceptions import FrewError, NodeError


def test_check_frew_path_type():
    with pytest.raises(FrewError):
        _check_frew_path(5)


def test_check_frew_path_exists():
    with pytest.raises(FrewError):
        _check_frew_path("path_does_not_exists.fwd")


def test_check_frew_path_extension():
    with pytest.raises(FrewError):
        _check_frew_path(os.path.join(TEST_DATA, "test_model_1.json"))


def test_check_json_path_type():
    with pytest.raises(FrewError):
        check_json_path(5)


def test_model_to_json():
    json_path = model_to_json(
        os.path.join(TEST_DATA, "convert_model_test.fwd")
    )
    path_exists = os.path.exists(json_path)
    os.remove(json_path)
    assert path_exists


def test_load_data():
    loaded_data = load_data(os.path.join(TEST_DATA, "test_model_1.json"))
    assert list(loaded_data.keys()) == [
        "OasysHeader",
        "JsonSchema",
        "File history",
        "Version",
        "Units",
        "Materials",
        "Struts",
        "Loads",
        "Stages",
        "Partial Factor Sets",
        "Node Generation",
        "Integral Bridge Data",
    ]


def test_check_json_path_exists():
    with pytest.raises(FrewError):
        check_json_path("path_does_not_exists.json")


def test_check_json_path_extension():
    with pytest.raises(FrewError):
        check_json_path(os.path.join(TEST_DATA, "test_model_1.fwd"))


def test_clear_results(json_data_with_results):
    json_data_without_results = clear_results(json_data_with_results)
    assert not json_data_without_results.get("Frew Results", False)


def test_titles_job_number(json_data):
    assert get_titles(json_data)["JobNumber"] == "261026"


def test_titles_job_title(json_data):
    assert get_titles(json_data)["JobTitle"] == "Elizabeth House "


def test_titles_initials(json_data):
    assert get_titles(json_data)["Initials"] == "FW"


def test_titles_key_error():
    with pytest.raises(FrewError):
        get_titles({"None": 1})


def test_titles_index_error():
    with pytest.raises(FrewError):
        get_titles({"OasysHeader": []})


def test_get_file_history_first(json_data):
    assert get_file_history(json_data)[0] == {
        "Date": "10-Jun-2020",
        "Time": "08:01",
        "Mode": "Edit",
        "User": "Fred.White",
        "Comments": "New",
    }


def test_get_file_history_third(json_data):
    assert get_file_history(json_data)[2] == {
        "Date": "10-Jun-2020",
        "Time": "09:06",
        "Mode": "Edit",
        "User": "Fred.White",
        "Comments": "Open",
    }


def test_get_file_history_key_error():
    with pytest.raises(FrewError):
        get_file_history({"None": 1})


def test_get_file_version(json_data):
    assert get_file_version(json_data) == "19.4.0.23"


def test_get_file_version_key_error():
    with pytest.raises(FrewError):
        get_file_version({"None": 1})


def test_get_file_version_index_error():
    with pytest.raises(FrewError):
        get_file_version({"OasysHeader": []})


def test_get_frew_version(json_data):
    assert get_frew_version(json_data) == "19.4"


def test_get_frew_version_key_error():
    with pytest.raises(FrewError):
        get_frew_version({"None": 1})


def test_get_frew_version_index_error():
    with pytest.raises(FrewError):
        get_frew_version({"OasysHeader": []})


def test_get_num_stages(json_data):
    assert get_num_stages(json_data) == 11


def test_get_num_stages_key_error():
    with pytest.raises(FrewError):
        get_num_stages({"None": 1})


def test_second_stage_name(json_data):
    assert (
        get_stage_names(json_data)[1] == " Install wall (900mm @ 1300mm C/C)"
    )


def test_fifth_stage_name(json_data):
    assert get_stage_names(json_data)[4] == (
        " Cast B02 floor slab (350mm thk @ -6.375mOD)"
    )


def test_ninth_stage_name(json_data):
    assert get_stage_names(json_data)[8] == (
        "  Cast B03 floor slab (2000mm thk @ -12.7mOD) - prop"
    )


def test_get_num_nodes(json_data):
    assert get_num_nodes(json_data) == 68


def test_get_num_nodes_none():
    example_dict = {"Stages": [{}]}
    assert get_num_nodes(example_dict) == 0


def test_get_num_nodes_different_per_stage():
    with pytest.raises(NodeError):
        example_dict = {
            "Stages": [
                {"GeoFrewNodes": ["Node1", "Node2"]},
                {"GeoFrewNodes": ["Node1", "Node2", "Node3"]},
            ]
        }
        get_num_nodes(example_dict)


def test_get_num_design_cases(json_data_with_results):
    assert get_num_design_cases(json_data_with_results) == 1


def test_get_num_design_cases_none(json_data):
    with pytest.raises(FrewError):
        get_num_design_cases(json_data)


def test_get_design_case_names(json_data_with_results):
    assert get_design_case_names(json_data_with_results) == ["SLS"]


def test_get_design_case_names_none(json_data):
    with pytest.raises(FrewError):
        get_design_case_names(json_data)


def test_check_results_present_none(json_data):
    with pytest.raises(FrewError):
        check_results_present(json_data)


def test_check_results_present(json_data_with_results):
    check_results_present(json_data_with_results)
    assert True
