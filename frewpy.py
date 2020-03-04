"""
frewpy
======

This module is a python wrapper for Oasys Frew, an embedded retaining wall
engineering design software.

"""

import win32com.client
from pprint import pprint


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
    wall : Class
        All wall related methods.
    struts : Class
        All strut related methods.
    soil : Class
        All soil related methods.
    water : Class
        All water related methods.

    """
    def __init__(self, file_path):
        self.model = win32com.client.Dispatch("frewLib.FrewComAuto")
        self.file_path = file_path
        self.model.Open(self.file_path)
        self.model.DeleteResults()

        # Initialise sub-classes as attributes of main model object
        self.wall = _Wall(self.model)
        self.struts = _Struts(self.model)
        self.soil = _Soil(self.model)
        self.water = _Water(self.model)

    def analyse(self):
        self.model.GetNumStages()
        self.model.Analyse(self.model.GetNumStages()-1)

    def close(self):
        self.model.Close()


class _Wall():
    """ A class to get and set information relating to wall nodes.

    ...

    Methods
    -------
    get_num_nodes()
    get_node_levels()

    Attributes
    ----------


    """

    def __init__(self, model):
        self.model = model

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

    def get_node_levels(self) -> dict:
        """ Function to get the levels of the nodes in a Frew model.

        Returns
        -------
        node_levels : dict
            The levels of each node in a Frew model.

        """
        node_levels = {}
        for node in range(0, self.get_num_nodes()):
            node_levels[node+1] = self.model.GetNodeLevel(node)
        return node_levels

    def get_results(self) -> dict:
        """ Function to get the shear, bending moment and displacement of the
        wall for each stage and node.

        Returns
        -------
        wall_results : dict
            The shear, bending and displacement of the wall.

        """
        wall_results = {}
        try:
            for stage in range(0, self.get_num_stages()):
                wall_results[stage+1] = {}
                for node in range(0, self.get_num_nodes()):
                    wall_results[stage+1][node+1] = [
                        self.model.GetNodeShear(node, stage),
                        self.model.GetNodeBending(node, stage),
                        self.model.GetNodeDisp(node, stage)
                    ]
        except Exception as e:
            wall_results = {}
            print(
                'Error! No results in model, please analyse the model first.'
            )
        return wall_results

    def get_wall_stiffness(self) -> dict:
        """ Function to get the stiffness of the wall for each stage and node.

        Returns
        -------
        wall_stiffness : dict
            The stiffness of the wall.

        """
        wall_stiffness = {}
        for stage in range(0, self.get_num_stages()):
            wall_stiffness[stage+1] = {}
            for node in range(0, self.get_num_nodes()):
                wall_stiffness[stage+1][node+1] = self.model.GetWallEI(
                    node,
                    stage
                )
        return wall_stiffness


class _Struts():
    """ A class to get and set information relating to struts.

    ...

    Methods
    -------

    Attributes
    ----------


    """

    def __init__(self, model):
        self.model = model


class _Soil():
    """ A class to get and set information relating to the soil.

    ...

    Methods
    -------

    Attributes
    ----------


    """

    def __init__(self, model):
        self.model = model


class _Water():
    """ A class to get and set information relating to the water.

    ...

    Methods
    -------

    Attributes
    ----------


    """

    def __init__(self, model):
        self.model = model
