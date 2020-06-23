import json
import os
from typing import Dict, List, Union

from .exceptions import FrewError


def _check_json_data(json_data: dict):
    if not json_data.get("Struts", False):
        raise FrewError("No struts defined in the model")


def _check_node_input_type(node: int):
    if type(node) != int:
        raise FrewError("Input node must be an integer.")


def get_struts(json_data: dict) -> List[dict]:
    """ Get a list of all the strut objects within the Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    struts : List[dict]
        A list of struts in the Frew model.

    """
    _check_json_data(json_data)
    return json_data["Struts"]


def get_strut_by_node(
    json_data: dict, node: int
) -> Dict[str, Union[float, int, bool]]:
    """ Get a strut object at the specified node location within the Frew
    model. If more than one strut is found, the first strut occurence is
    returned.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.
    node : int
        The node number of the strut

    Returns
    -------
    strut : Dict[str, Union[float, int, bool]]
        A strut object represented as a dictionary in the Frew model matching
        the input node number.

    """
    _check_node_input_type(node)
    _check_json_data(json_data)

    for strut in get_struts(json_data):
        if strut["NodeStrut"] == node:
            return strut

    raise FrewError(f"There is no strut defined at node {node} in the model")


def get_struts_by_node(json_data: dict, node: int) -> List[dict]:
    """ Get a list of strut objects at the specified node location within the
    Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.
    node : int
        The node number of the strut

    Returns
    -------
    struts : Dict[str, Union[float, int, bool]]
        A list of struts in the Frew model that match the input node number.

    """
    _check_node_input_type(node)
    _check_json_data(json_data)

    struts = [
        strut for strut in get_struts(json_data) if strut["NodeStrut"] == node
    ]
    if struts:
        return struts
    else:
        raise FrewError(
            f"There are no struts defined at node {node} in the model"
        )
