"""
frewpy
======

This module is a python wrapper for Oasys Frew, an embedded retaining wall
engineering design software.

"""

import os
import json
from typing import Dict, List, Union
from uuid import uuid4

from comtypes.client import CreateObject  # type: ignore
from _ctypes import COMError  # type: ignore

from frewpy.models import Wall, Soil, Water, Calculation, Strut
from frewpy.utils import (
    check_json_path,
    load_data,
    get_titles,
    get_file_history,
    get_file_version,
    get_frew_version,
    get_num_stages,
    get_stage_names,
    get_num_nodes,
)
from frewpy.models.exceptions import (
    FrewError,
)


class FrewModel:
    """ A class used to establish a connection to any Frew model and to
    manipulate it as required using simple pythonic object oriented syntax.
    ...

    Attributes
    ----------
    file_path : str
        The absolute file path to the Frew model.
    folder_path : str
        The absolute folder path to the Frew model, not including the file
        name.
    wall : class
        All wall related methods associated with a Frew model.
    soil : class
        All soil related methods associated with a Frew model.
    water : class
        All water related methods associated with a Frew model.
    calculation : class
        All calculation methods based on Frew results.
    strut : class
        All strut related methods associated with a Frew model.

    Methods
    -------
    get(request: str)
        Method to get information about the model. Request can be: 'titles',
        'file history', 'file version', 'frew version', 'num stages', 'stage
        names', 'num nodes'.
    analyse()
        Analyse the model using the COM interface to open Frew. This method
        requires greater than Frew 19.4 Build 24.
    save(save_path: str = None)
        Saves the current json Frew model to the original file or to a new path
        if provided to the method.

    """
    def __init__(self, file_path: str) -> None:
        check_json_path(file_path)

        self.file_path: str = file_path
        self.json_data: Dict[str, list] = load_data(self.file_path)
        self.wall = Wall(self.json_data)
        self.soil = Soil(self.json_data)
        self.water = Water(self.json_data)
        self.calculation = Calculation(self.json_data)
        self.strut = Strut(self.json_data)

    def get(self, request: str) -> Union[dict, str, int, list]:
        """ Method to get information about the model.

        Parameters
        ----------
        request : str
            Options for request are: 'titles', 'file history', 'file version',
            'frew version', 'num stages', 'stage names', 'num nodes'.

        Returns
        -------
        return_value : Union[dict, str, int, list]
            The information requested about the model.

        """
        if type(request) != str:
            raise FrewError('Request must be a string.')
        if request == 'titles':
            return get_titles(self.json_data)
        elif request == 'file history':
            return get_file_history(self.json_data)
        elif request == 'file version':
            return get_file_version(self.json_data)
        elif request == 'frew version':
            return get_frew_version(self.json_data)
        elif request == 'num stages':
            return get_num_stages(self.json_data)
        elif request == 'stage names':
            return get_stage_names(self.json_data)
        elif request == 'num nodes':
            return get_num_nodes(self.json_data)
        else:
            raise FrewError('Please input a valid option.')

    def analyse(self) -> None:
        """ Method to open the COM object, analyse it, save it, and close
        the object.

        """
        num_stages: int = get_num_stages(self.json_data)
        folder_path: str = os.path.dirname(self.file_path)
        temp_file_path: str = os.path.join(folder_path, f'{uuid4()}.json')
        self.save(temp_file_path)
        try:
            model = CreateObject('frewLib.FrewComAuto')
        except OSError:
            os.remove(temp_file_path)
            raise FrewError('Failed to create a COM object.')
        try:
            model.Open(temp_file_path)
        except COMError:
            os.remove(temp_file_path)
            raise FrewError('Failed to open the Frew model.')
        model.DeleteResults()
        model.Analyse(num_stages)
        model.SaveAs(temp_file_path)
        model.Close()
        new_data: Dict[str, list] = load_data(temp_file_path)
        os.remove(temp_file_path)
        self._clear_json_data()
        self._refill_json_data(new_data)

    def save(self, save_path: str = None) -> None:
        """ A method to save the current json data.

        Parameters
        ----------
        save_path : str, optional
            The path including file name (.json) for the data to be saved to.
            If this is not provided, the model at the original file path will
            be overwritten.

        """
        if save_path:
            if (
                    type(save_path) == str
                    and save_path.lower().endswith('.json')
            ):
                try:
                    with open(save_path, 'w') as f:
                        f.write(json.dumps(self.json_data))
                except FileNotFoundError:
                    raise FileNotFoundError('''
                        Unable to save the model. File path is invalid.
                    ''')
            else:
                raise FrewError('''
                    Unable to save the model. File path must be a valid string
                    and end with ".json".
                ''')
        else:
            with open(self.file_path, 'w') as f:
                f.write(json.dumps(self.json_data))

    def _clear_json_data(self):
        keys: List[str] = list(self.json_data.keys())
        for key in keys:
            del self.json_data[key]

    def _refill_json_data(self, new_data):
        for key in new_data.keys():
            self.json_data[key] = new_data[key]
