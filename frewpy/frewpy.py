"""
frewpy
======

This module is a python wrapper for Oasys Frew, an embedded retaining wall
engineering design software.

"""

import os

import win32com.client

from frewpy.models import (
    FrewError,
    _Wall,
    _Struts,
    _Soil,
    _Water,
    _Calculations,
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
    get_num_nodes()
        To get the number of nodes in a Frew model.
    get_num_stages()
        To get the number of stages in a Frew model.

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
        self.model = win32com.client.Dispatch("frewLib.FrewComAuto")
        self.file_path = file_path
        self.folder_path = os.path.dirname(self.file_path)
        self.model.Open(self.file_path)
        self.model.DeleteResults()

        self.num_nodes = self.get_num_nodes()
        self.num_stages = self.get_num_stages()

        # Initialise sub-classes as attributes of main model object
        self.wall = _Wall(
            self.model,
            self.file_path,
            self.folder_path,
            self.num_nodes,
            self.num_stages
        )
        self.struts = _Struts(self.model, self.file_path, self.folder_path)
        self.soil = _Soil(
            self.model,
            self.file_path,
            self.folder_path,
            self.num_nodes,
            self.num_stages
        )
        self.water = _Water(
            self.model,
            self.file_path,
            self.folder_path,
            self.num_nodes,
            self.num_stages
        )
        self.calculate = _Calculations(
            self.model,
            self.file_path,
            self.folder_path,
            self.num_nodes,
            self.num_stages
        )

    def analyse(self):
        self.model.GetNumStages()
        self.model.Analyse(self.model.GetNumStages()-1)

    def close(self):
        self.model.Close()

    def get_num_nodes(self) -> int:
        """ Function to get the number of nodes in a Frew model.

        Returns
        -------
        num_nodes : int
            The number of nodes in a Frew model.

        """
        num_nodes = self.model.GetNumNodes()
        return num_nodes

    def get_num_stages(self) -> int:
        """ Function to get the number of stages in a Frew model.

        Returns
        -------
        num_stages : int
            The number of stages in a Frew model.

        """
        num_stages = self.model.GetNumStages()
        return num_stages
