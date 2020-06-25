"""
frewpy
======

This module is a python wrapper for Oasys Frew, an embedded retaining wall
engineering design software.

"""

import os
import json

from typing import Dict, List, Union

from frewpy.models import Wall, Soil, Water, Calculation, Strut
from frewpy.utils import check_extension, load_data
from frewpy.models.exceptions import (
    FrewError,
    NodeError,
    FrewpyFileExtensionNotRecognised,
)


class FrewModel:
    """ A class used to establish a connection to any Frew model and to
    manipulate it as required using simple pythonic object oriented syntax.

    ...

    Attributes
    ----------
    file_extension : str
        The file extension of the Frew model.
    file_history : List[Dict[str, str]]
        Records of when the file has been opened in Frew and by which user.
    file_name : str
        The file name of the Frew model including extension.
    file_path : str
        The absolute file path to the Frew model.
    file_version : str
        The version of the model file showing the exact build of Frew.
    folder_path : str
        The absolute folder path to the Frew model, not including the file
        name.
    frew_version : str
        The overall Frew version in which the model was created.
    json_data : Dict[str, list]
        The Frew model data loaded in as a Python dictionary.
    num_nodes : int
        The number of nodes in the Frew model. This is common across all stages
        of the Frew model.
    num_stages : int
        The number of stages in the Frew model.
    stage_names : List[str]
        The names of all the stages in the Frew model.
    titles : Dict[str, str]
        The project titles including Job Number, Job Title, Sub Title,
        Calculation Heading, Initials, and Notes.

    """

    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path

        if not os.path.exists(self.file_path):
            raise FrewError("Frew model file path does not exists.")
        self.file_extension: str = check_extension(self.file_path)
        self.json_data: Dict[str, list] = load_data(self.file_path)
        self.wall = Wall(self.json_data)
        self.soil = Soil(self.json_data)
        self.water = Water(self.json_data)
        self.calculation = Calculation(self.json_data)
        self.strut = Strut(self.json_data)

    #     if self.file_extension == 'fwd':
    #         self.file_path = self._model_to_json()

    #     self.file_name: str = os.path.basename(self.file_path)
    #     self.folder_path: str = os.path.dirname(self.file_path)

    #     # Get key information from json file
    #     self.titles: Dict[str, str] = core.get_titles(self.json_data)
    #     self.file_history: List[Dict[str, str]] = core.get_file_history(
    #         self.json_data,
    #     )
    #     self.file_version: str = core.get_file_version(self.json_data)
    #     self.frew_version: str = core.get_frew_version(self.json_data)
    #     self.num_stages: int = core.get_num_stages(self.json_data)
    #     self.stage_names: List[str] = core.get_stage_names(
    #         self.json_data,
    #         self.num_stages,
    #     )
    #     self.num_nodes: int = core.get_num_nodes(
    #         self.json_data,
    #         self.num_stages,
    #     )

    # def _model_to_json(self) -> str:
    # self.file_extension = 'json'
    # file_path_without_extension = self.file_path.rsplit('.', 1)[0]
    # model = win32com.client.Dispatch("frewLib.FrewComAuto")
    # if model.Open(self.file_path) == -1:
    #     raise FrewError(
    #         'Frew model failed to open.'
    #     )
    # else:
    # model.Open(self.file_path)
    # new_file_path = (
    #     f'{file_path_without_extension}.{self.file_extension}'
    # )
    # try:
    #     model.SaveAs(new_file_path)
    # except Exception as e:
    #     pass
    # model.Close()
    # return new_file_path

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
