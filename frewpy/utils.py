import json
import os
import numpy as np  # type: ignore
from typing import Dict, List

from comtypes.client import CreateObject  # type: ignore
from _ctypes import COMError  # type: ignore

from frewpy.models.exceptions import (
    FrewError,
    NodeError
)


def _check_frew_path(file_path):
    if type(file_path) != str:
        raise FrewError('The path must be a string.')
    if not os.path.exists(file_path):
        raise FrewError('Path to Frew model does not exist.')
    if not file_path.lower().endswith('.fwd'):
        raise FrewError('Path must be to a valid Frew model.')


def model_to_json(file_path) -> str:
    """ Converts a `.fwd` Frew model to a `.json` Frew model.

    Parameters
    ----------
    file_path : str
        Absolute file path to the '.fwd' Frew model.

    Returns
    -------
    json_path : str
        The new file path of the json file.

    """
    _check_frew_path(file_path)
    json_path: str = f'{file_path.rsplit(".", 1)[0]}.json'
    try:
        model = CreateObject('frewLib.FrewComAuto')
    except OSError:
        os.remove(file_path)
        raise FrewError('Failed to create a COM object.')
    try:
        model.Open(file_path)
    except COMError:
        raise FrewError('Failed to open the Frew model.')
    model.SaveAs(json_path)
    model.Close()
    return json_path


def check_json_path(file_path: str):
    """ Checks whether the file extension is a json.

    Parameters
    ----------
    file_path : str
        Absolute file path to the Frew model.

    Returns
    -------
    None

    """
    if type(file_path) != str:
        raise FrewError(f'''
            File path must be a string. Value {file_path} of type {type
            (file_path)} given.
        ''')
    if not os.path.exists(file_path):
        raise FrewError('Frew model file path does not exists.')
    if not file_path.lower().endswith('.json'):
        raise FrewError('''
            File extension must be a .json. Please use model_to_json to
            convert it. Import this function from frewpy.utils.
        ''')


def load_data(file_path: str) -> dict:
    """ Loads the json file in as a Python dictionary.

    Parameters
    ----------
    file_path : str
        Absolute file path to the Frew model.

    Returns
    -------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    """
    with open(file_path) as file:
        return json.loads(file.read())


def clear_results(json_data: dict) -> dict:
    """ Clears the results in the json file so that it can be analysed using
    the COM interface.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    json_data : dict
        A Python dictionary of the data held within the json model file without
        the results.

    """
    if json_data.get('Frew Results', False):
        del json_data['Frew Results']
    return json_data


def get_titles(json_data: dict) -> Dict[str, str]:
    """ Returns the titles within the json model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    titles : Dict[str, str]
        The project titles including Job Number, Job Title, Sub Title,
        Calculation Heading, Initials, and Notes.

    """
    try:
        return json_data['OasysHeader'][0]['Titles'][0]
    except KeyError:
        raise FrewError('Unable to retreive title information.')
    except IndexError:
        raise FrewError('Unable to retreive title information.')


def get_file_history(json_data: dict) -> List[Dict[str, str]]:
    """ Returns the file history of the Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    file_history : List[Dict[str, str]]
        Records of when the file has been opened in Frew and by which user.

    """
    try:
        return json_data['File history']
    except KeyError:
        raise FrewError('Unable to retreive file history.')


def get_file_version(json_data: Dict[str, list]) -> str:
    """ Returns the file version of the Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    file_version : str
        The version of the model file showing the exact build of Frew.

    """
    try:
        return (
            json_data['OasysHeader'][0]['Program title'][0][
                'FileVersion'
            ])
    except KeyError:
        raise FrewError('Unable to retreive file version.')
    except IndexError:
        raise FrewError('Unable to retreive file version.')


def get_frew_version(json_data: dict) -> str:
    """ Returns the frew version required for the Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    frew_version : str
        The overall Frew version in which the model was created.

    """
    try:
        return json_data[
            'OasysHeader'
        ][0]['Program title'][0]['Version']
    except KeyError:
        raise FrewError('Unable to retreive Frew model version.')
    except IndexError:
        raise FrewError('Unable to retreive Frew model version.')


def get_num_stages(json_data: dict) -> int:
    """ Returns the number of stages in the model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    num_stages : int
        The number of stages in the Frew model.

    """
    try:
        return len(json_data['Stages'])
    except KeyError:
        raise FrewError('Unable to retrieve the number of stages.')


def get_stage_names(json_data: dict) -> List[str]:
    """ Returns the names of the stages within the Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    stage_names : List[str]
        A list of the names of stages within the Frew model.

    """
    num_stages: int = get_num_stages(json_data)
    return [json_data['Stages'][stage]['Name'] for stage in range(num_stages)]


def get_num_nodes(json_data: dict) -> int:
    """ Returns the number of nodes in the Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    num_nodes : int
        The number of nodes present in each stage. This will always
        just be 1 integer, and the function will raise an error if it is not
        the same for every stage.

    """
    num_stages = get_num_stages(json_data)
    num_nodes: List[int] = []
    for stage in range(num_stages):
        if not json_data['Stages'][stage].get('GeoFrewNodes', False):
            return 0
        num_nodes.append(
            len(json_data['Stages'][stage]['GeoFrewNodes'])
        )
        unique_num_nodes = np.unique(np.array(num_nodes))
    if len(unique_num_nodes) == 1:
        return unique_num_nodes[0]
    else:
        raise NodeError(
            'Number of nodes is not unique for every stage.'
        )


def get_num_design_cases(json_data: dict) -> int:
    """ Returns the number of design cases present in the model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    num_design_cases : int
        The number of design cases in the Frew model.

    """
    return len(json_data['Frew Results'])


def get_design_case_names(json_data: dict) -> List[str]:
    """ Returns the names of the design cases present in the model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    design_case_names : List[str]
        The names of the design cases in the Frew model.

    """
    return [
        design_case[
            'GeoPartialFactorSet'
        ]['Name'] for design_case in json_data['Frew Results']
    ]
