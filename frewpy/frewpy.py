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

from frewpy.models import (
    _Wall,
    _Struts,
    _Soil,
    _Water,
    _Calculations,
)
from frewpy.models.exceptions import (
    FrewError,
    NodeError,
)


class FrewModel():
    """ A class used to establish a connection to any Frew model and to
    manipulate it as required using pythonic terms and OOP.

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
        self._check_path()
        self.file_extension = self._check_extension()
        self.model = win32com.client.Dispatch("frewLib.FrewComAuto")
        if self.file_extension == 'fwd':
            self.file_path = self._model_to_json()

        self.json_data = self._load_data()
        self._clear_results()

        self.file_name = os.path.basename(self.file_path)
        self.folder_path = os.path.dirname(self.file_path)

        # Get key information from json file
        self.titles = self._get_titles()
        self.file_history = self._get_file_history()
        self.file_version = self._get_file_version()
        self.version = self._get_model_version()
        self.materials = self._get_materials()
        self.num_stages = self._get_num_stages()
        self.stage_names = self._get_stage_names()
        self.num_nodes = self._get_num_nodes()


        # Initialise sub-classes as attributes of main model object
        # self.wall = _Wall(
        #     self.model,
        #     self.file_path,
        #     self.folder_path,
        #     self.num_nodes,
        #     self.num_stages
        # )
        # self.struts = _Struts(self.model, self.file_path, self.folder_path)
        # self.soil = _Soil(
        #     self.model,
        #     self.file_path,
        #     self.folder_path,
        #     self.num_nodes,
        #     self.num_stages
        # )
        # self.water = _Water(
        #     self.model,
        #     self.file_path,
        #     self.folder_path,
        #     self.num_nodes,
        #     self.num_stages
        # )
        # self.calculate = _Calculations(
        #     self.model,
        #     self.file_path,
        #     self.folder_path,
        #     self.num_nodes,
        #     self.num_stages
        # )



    def _check_path(self) -> None:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError

    def _check_extension(self) -> str:
        file_extension = os.path.basename(
            self.file_path
        ).rsplit('.', 1)[1].lower()
        if file_extension not in ['fwd', 'json']:
            raise FrewError(
                'File extension must be either .json or .fwd'
            )
        else:
            return file_extension

    def _model_to_json(self) -> str:
        self.file_extension = 'json'
        file_path_without_extension = self.file_path.rsplit('.', 1)[0]

        if self.model.Open(self.file_path) == -1:
            raise FrewError(
                'Frew model failed to open.'
            )
        else:
            new_file_path = (
                f'{file_path_without_extension}.{self.file_extension}'
            )
            self.model.Open(self.file_path)
            try:
                self.model.SaveAs(new_file_path)
            except Exception as e:
                pass
            self.model.Close()
            return new_file_path

    def _load_data(self) -> dict:
        with open(self.file_path) as file:
            json_data = json.loads(file.read())
        return json_data

    def _clear_results(self) -> None:
        if self.json_data.get('Frew Results', False):
            del self.json_data['Frew Results']

    def _get_titles(self) -> dict:
        try:
            titles = self.json_data['OasysHeader'][0]['Titles'][0]
        except KeyError:
            raise FrewError('Unable to retreive title information.')
        except IndexError:
            raise FrewError('Unable to retreive title information.')
        return titles

    def _get_file_history(self) -> list:
        try:
            file_history = self.json_data['File history']
        except KeyError:
            raise FrewError('Unable to retreive file history.')
        return file_history

    def _get_file_version(self) -> str:
        try:
            file_version = self.json_data['OasysHeader'][0]['Program title'][0][
                'FileVersion'
            ]
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

    def _get_materials(self) -> list:
        materials = []
        if not self.json_data.get('Materials', False):
            raise FrewError('No materials defined in the model')
        for material_dict in self.json_data['Materials']:
            materials.append(material_dict['Name'])
        return materials

    def _get_num_stages(self) -> int:
        num_stages = len(self.json_data['Stages'])
        return num_stages

    def _get_stage_names(self) -> list:
        stage_names = []
        for stage in range(0, self.num_stages):
            stage_names.append(self.json_data['Stages'][stage]['Name'])
        return stage_names

    def _get_num_nodes(self) -> int:
        num_nodes = []
        for stage in range(0, self.num_stages):
            num_nodes.append(
                len(self.json_data['Stages'][stage]['GeoFrewNodes'])
            )
        unique_num_nodes = np.unique(np.array(num_nodes))
        if len(unique_num_nodes) == 1:
            return unique_num_nodes[0]
        else:
            raise NodeError(
                'Number of nodes is not unique for every stage.'
            )

    def get_material_properties(self, material: str) -> dict:
        if not self.json_data.get('Materials', False):
            raise FrewError('No materials defined in the model')
        material_properties = False
        for material_dict in self.json_data['Materials']:
            if material_dict['Name'] == material:
                flag = True
                material_properties = material_dict
        if not material_properties:
            raise FrewError(f'No material called {material} in the model.')
        return material_properties

    def analyse(self) -> None:
        """ Function to open the COM object, analyse it, save it, and close the
        object.

        """
        self.model.Open(self.file_path)
        self.model.Analyse(self.num_stages-1)
        self.model.Save()
        self.model.Close()
        self.json_data = self._load_data()
