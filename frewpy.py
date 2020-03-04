"""
frewpy
======

This module is a python wrapper for Oasys Frew, an embedded retaining wall
engineering design software.

"""

import win32com.client


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


    Attributes
    ----------


    """

    def __init__(self, model):
        self.model = model

    def get_num_nodes(self):
        return self.model.GetNumNodes()


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
