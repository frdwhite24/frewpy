"""
frewpy
======

This module is a python wrapper for Oasys Frew, an embedded retaining wall
engineering design software.

"""

import os
import json

import win32com.client
import numpy as np

from frewpy.models.core import (
    core_check_path,
    core_check_extension,
    core_load_data,
    core_clear_results,
    core_get_titles,
    core_get_num_stages,
    core_get_num_nodes,
    core_get_stage_names,
)
from frewpy.models.soil import (
    soil_get_materials,
    soil_get_material_properties
)
from frewpy.models.exceptions import (
    FrewpyFileExtensionNotRecognised,
    FrewError,
    NodeError,
)


class FrewModel():
    """ A class used to establish a connection to any Frew model and to
    manipulate it as required using pythonic terminology.

    ...

    Methods
    -------
    analyse()
        To run the analysis on a Frew model.
    close()
        To close the COM connection to a Frew model.

    Attributes
    ----------
    wall : FrewModel._Wall
        All wall related methods.
    struts : FrewModel._Struts
        All strut related methods.
    soil : FrewModel._Soil
        All soil related methods.
    water : FrewModel._Water
        All water related methods.

    """
    def __init__(self, file_path):
        self.file_path = file_path

        # Run checks, convert model to json file, remove results
        self.path_exists = core_check_path(self.file_path)
        self.file_extension = core_check_extension(self.file_path)
        self.json_data = core_load_data(self.file_path)
        # if self.file_extension == 'fwd':
        #     self.file_path = self._model_to_json()

        # self.file_name = os.path.basename(self.file_path)
        # self.folder_path = os.path.dirname(self.file_path)

        # # Get key information from json file
        self.titles = core_get_titles(self.json_data)
        # self.file_history = self._get_file_history()
        # self.file_version = self._get_file_version()
        # self.version = self._get_model_version()
        self.num_stages = core_get_num_stages(self.json_data)
        self.stage_names = core_get_stage_names(
            self.json_data,
            self.num_stages
        )
        self.num_nodes = core_get_num_nodes(
            self.json_data,
            self.num_stages
        )

    def _get_file_history(self) -> list:
        try:
            file_history = self.json_data['File history']
        except KeyError:
            raise FrewError('Unable to retreive file history.')
        return file_history

    def _get_file_version(self) -> str:
        try:
            file_version = (
                self.json_data['OasysHeader'][0]['Program title'][0][
                    'FileVersion'
                ])
        except KeyError:
            raise FrewError('Unable to retreive file version.')
        except IndexError:
            raise FrewError('Unable to retreive file version.')
        return file_version

    def _get_model_version(self) -> str:
        try:
            model_version = self.json_data[
                'OasysHeader'
            ][0]['Program title'][0]['Version']
        except KeyError:
            raise FrewError('Unable to retreive Frew model version.')
        except IndexError:
            raise FrewError('Unable to retreive Frew model version.')
        return model_version

    def get_materials(self) -> list:
        return soil_get_materials(self.json_data)

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
    #     self.json_data = core_clear_results(self.json_data)
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
