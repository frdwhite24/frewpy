import json
import os
import numpy as np

from .exceptions import FrewpyFileExtensionNotRecognised, FrewError


def core_check_path(file_path: str) -> bool:
    """ Checks the file path exists.

    Parameters
    ----------
    file_path : str
        Absolute file path to the Frew model.

    Returns
    -------
    bool
        Returns True if the file path exists.

    """
    if not os.path.exists(file_path):
        raise FileNotFoundError
    else:
        return True


def core_check_extension(file_path: str) -> str:
    """ Checks whether the file extension is in the list of accepted file
    extensions.

    Parameters
    ----------
    file_path : str
        Absolute file path to the Frew model.

    Returns
    -------
    file_extension : str
        The file extension of the file path passed into the function.

    """
    file_extension = os.path.basename(
        file_path
    ).rsplit('.', 1)[1].lower()
    if file_extension not in ['json']:
        raise FrewpyFileExtensionNotRecognised(
            'File extension must be a .json'
        )
    else:
        return file_extension


def core_load_data(file_path: str) -> dict:
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
        json_data = json.loads(file.read())
    return json_data


def core_clear_results(json_data: dict) -> dict:
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


def core_get_titles(json_data: dict) -> dict:
    """ Returns the titles within the json model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    titles : dict
        A dictionary containing all the titles information for the model.

    """
    try:
        titles = json_data['OasysHeader'][0]['Titles'][0]
    except KeyError:
        raise FrewError('Unable to retreive title information.')
    except IndexError:
        raise FrewError('Unable to retreive title information.')
    return titles


def core_get_num_stages(json_data: dict) -> int:
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
    num_stages = len(json_data['Stages'])
    return num_stages


def core_get_stage_names(json_data: dict, num_stages: int) -> list:
    """ Returns the names of the stages within the Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.
    num_stages : int
        The number of stages in the Frew model.

    Returns
    -------
    stage_names : list
        A list of the names of stages within the Frew model.

    """
    stage_names = []
    for stage in range(0, num_stages):
        stage_names.append(json_data['Stages'][stage]['Name'])
    return stage_names


def core_get_num_nodes(json_data: dict, num_stages: int) -> int:
    """ Returns the number of nodes in the Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.
    num_stages : int
        The number of stages in the Frew model.

    Returns
    -------
    unique_num_nodes : int
        The number of nodes which are present in each stage. This will always
        just be 1 integer, and the function will raise an error if it is not
        the same for every stage.

    """
    num_nodes = []
    for stage in range(0, num_stages):
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
