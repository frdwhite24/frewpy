import json
import os
import numpy as np  # type: ignore
from typing import Dict, List

from .exceptions import FrewpyFileExtensionNotRecognised, FrewError, NodeError


def check_path(file_path: str) -> bool:
    """ Checks the file path exists.

    Parameters
    ----------
    file_path : str
        Absolute file path to the Frew model.

    Returns
    -------
    path_exists : bool
        Returns True if the file path exists.

    """
    if not os.path.exists(file_path):
        raise FileNotFoundError
    else:
        return True


def check_extension(file_path: str) -> str:
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
    file_extension: str = os.path.basename(
        file_path
    ).rsplit('.', 1)[1].lower()
    if file_extension not in ['json']:
        raise FrewpyFileExtensionNotRecognised(
            'File extension must be a .json'
        )
    else:
        return file_extension


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
    titles : dict
        A dictionary containing all the titles information for the model.

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
    file_history : list
        The file history of the Frew model.

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
    file_version : list
        The file version of the Frew model.

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
    return len(json_data['Stages'])


def get_stage_names(json_data: dict, num_stages: int) -> List[str]:
    """ Returns the names of the stages within the Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.
    num_stages : int
        The number of stages in the Frew model.

    Returns
    -------
    stage_names : List[str]
        A list of the names of stages within the Frew model.

    """
    return [json_data['Stages'][stage]['Name'] for stage in range(num_stages)]


def get_num_nodes(json_data: dict, num_stages: int) -> int:
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


# def _model_to_json(self) -> str:
#     self.file_extension = 'json'
#     file_path_without_extension = self.file_path.rsplit('.', 1)[0]
#     model = win32com.client.Dispatch("frewLib.FrewComAuto")
#     if model.Open(self.file_path) == -1:
#         raise FrewError(
#             'Frew model failed to open.'
#         )
#     else:
#     model.Open(self.file_path)
#     new_file_path = (
#         f'{file_path_without_extension}.{self.file_extension}'
#     )
#     try:
#         model.SaveAs(new_file_path)
#     except Exception as e:
#         pass
#     model.Close()
#     return new_file_path


# def analyse(self) -> None:
#     """ Function to open the COM object, analyse it, save it, and close
# the
#     object.

#     """
#     self.json_data = clear_results(self.json_data)
#     self.save()
#     model = win32com.client.Dispatch("frewLib.FrewComAuto")
#     model.Open(self.file_path)
#     if model.Open(self.file_path) == -1:
#         raise FrewError(
#             'Frew model failed to open.'
#         )
#     model.Analyse(self.num_stages-1)
#     model.Save()
#     model.Close()
#     self.json_data = self._load_data()


# def save(self, save_path: str = None) -> None:
#     """ A method to save the current json data.

#     Parameters
#     ----------
#     save_path : str, optional
#         The path including file name (.json) for the data to be saved to.
#         If this is not provided, the model at the original file path will
#         be overwritten.

#     """
#     if save_path:
#         if not type(save_path) == str or not save_path.endswith('.json'):
#             raise FrewError('''
#                 Unable to save the model. File path must be a valid string
#                 and end with ".json".
#             ''')
#         try:
#             with open(save_path, 'w') as f:
#                 f.write(json.dumps(self.json_data))
#         except FileNotFoundError:
#             raise FileNotFoundError('''
#                 Unable to save the model. File path is invalid.
#             ''')
#     else:
#         with open(self.file_path, 'w') as f:
#             f.write(json.dumps(self.json_data))
