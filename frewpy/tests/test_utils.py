import os
import json

import pytest

from test_config import TEST_DATA
from test_fixtures import json_data
from frewpy.utils import (
    _check_frew_path,
    check_json_path,
    get_titles,
    get_file_history,
    get_file_version,
    get_frew_version,
    get_num_stages,
    get_stage_names,
    get_num_nodes,
)
from frewpy.models.exceptions import FrewError, NodeError


def test_check_frew_path_type():
    with pytest.raises(FrewError):
        _check_frew_path(5)


def test_check_frew_path_exists():
    with pytest.raises(FrewError):
        _check_frew_path('path_does_not_exists.fwd')


def test_check_frew_path_extension():
    with pytest.raises(FrewError):
        _check_frew_path(os.path.join(TEST_DATA, 'test_model_1.json'))


def test_check_json_path_type():
    with pytest.raises(FrewError):
        check_json_path(5)


def test_check_json_path_exists():
    with pytest.raises(FrewError):
        check_json_path('path_does_not_exists.json')


def test_check_json_path_extension():
    with pytest.raises(FrewError):
        check_json_path(os.path.join(TEST_DATA, 'test_model_1.fwd'))


def test_titles_job_number(json_data):
    assert get_titles(json_data)['JobNumber'] == '261026'


def test_titles_job_title(json_data):
    assert get_titles(json_data)['JobTitle'] == 'Elizabeth House '


def test_titles_initials(json_data):
    assert get_titles(json_data)['Initials'] == 'FW'


def test_titles_key_error():
    with pytest.raises(FrewError):
        get_titles({'None': 1})


def test_titles_index_error():
    with pytest.raises(FrewError):
        get_titles({'OasysHeader': []})


def test_get_file_history_first(json_data):
    assert get_file_history(json_data)[0] == {
        "Date": "10-Jun-2020",
        "Time": "08:01",
        "Mode": "Edit",
        "User": "Fred.White",
        "Comments": "New"
    }


def test_get_file_history_third(json_data):
    assert get_file_history(json_data)[2] == {
        "Date": "10-Jun-2020",
        "Time": "09:06",
        "Mode": "Edit",
        "User": "Fred.White",
        "Comments": "Open"
    }


def test_get_file_history_key_error():
    with pytest.raises(FrewError):
        get_file_history({'None': 1})


def test_get_file_version(json_data):
    assert get_file_version(json_data) == '19.4.0.23'


def test_get_file_version_key_error():
    with pytest.raises(FrewError):
        get_file_version({'None': 1})


def test_get_file_version_index_error():
    with pytest.raises(FrewError):
        get_file_version({'OasysHeader': []})


def test_get_frew_version(json_data):
    assert get_frew_version(json_data) == '19.4'


def test_get_frew_version_key_error():
    with pytest.raises(FrewError):
        get_frew_version({'None': 1})


def test_get_frew_version_index_error():
    with pytest.raises(FrewError):
        get_frew_version({'OasysHeader': []})


def test_get_num_stages(json_data):
    assert get_num_stages(json_data) == 11


def test_get_num_stages_key_error():
    with pytest.raises(FrewError):
        get_num_stages({'None': 1})


def test_second_stage_name(json_data):
    assert (
        get_stage_names(json_data)[1] == ' Install wall (900mm @ 1300mm C/C)'
    )


def test_fifth_stage_name(json_data):
    assert get_stage_names(json_data)[4] == (
        ' Cast B02 floor slab (350mm thk @ -6.375mOD)'
    )


def test_ninth_stage_name(json_data):
    assert get_stage_names(json_data)[8] == (
        '  Cast B03 floor slab (2000mm thk @ -12.7mOD) - prop'
    )


def test_get_num_nodes(json_data):
    assert get_num_nodes(json_data) == 68


def test_get_num_nodes_none():
    json_data = {
        'Stages': [
            {},
        ]
    }
    assert get_num_nodes(json_data) == 0


def test_get_num_nodes_different_per_stage():
    with pytest.raises(NodeError):
        json_data = {
            'Stages': [
                {'GeoFrewNodes': ['Node1', 'Node2']},
                {'GeoFrewNodes': ['Node1', 'Node2', 'Node3']},
            ]
        }
        get_num_nodes(json_data)
