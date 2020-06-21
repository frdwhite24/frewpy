"""
frewpy
======

This module is a python wrapper for Oasys Frew, an embedded retaining wall
engineering design software.

"""

import os
import json

from typing import Dict, List

from frewpy.models import soil, core, wall
from frewpy.models.exceptions import (
    FrewError,
    NodeError,
    FrewpyFileExtensionNotRecognised,
)


class FrewModel:
    """ A class used to establish a connection to any Frew model and to
    manipulate it as required using simple pythonic object oriented syntax.

    ...

    Methods
    -------
    get_materials()
        Get a list of materials used within the Frew model.

    Attributes
    ----------
    file_path : str
        The absolute file path to the Frew model.
    file_extension : str
        The file extension of the Frew model.
    json_data : Dict[str, list]
        The Frew model data loaded in as a Python dictionary.
    file_name : str
        The file name of the Frew model including extension.
    folder_path : str
        The absolute folder path to the Frew model, not including the file
        name.
    titles : Dict[str, str]
        The project titles including Job Number, Job Title, Sub Title,
        Calculation Heading, Initials, and Notes.
    file_history : List[Dict[str, str]]
        Records of when the file has been opened in Frew and by which user.
    file_version : str
        The version of the model file showing the exact build of Frew.
    frew_version : str
        The overall Frew version in which the model was created.
    num_stages : int
        The number of stages in the Frew model.
    stage_names : List[str]
        The names of all the stages in the Frew model.
    num_nodes : int
        The number of nodes in the Frew model. This is common across all stages
        of the Frew model.

    """
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path

        path_exists: bool = core.check_path(self.file_path)
        self.file_extension: str = core.check_extension(self.file_path)
        self.json_data: Dict[str, list] = core.load_data(self.file_path)
        # if self.file_extension == 'fwd':
        #     self.file_path = self._model_to_json()

        self.file_name: str = os.path.basename(self.file_path)
        self.folder_path: str = os.path.dirname(self.file_path)

        # Get key information from json file
        self.titles: Dict[str, str] = core.get_titles(self.json_data)
        self.file_history: List[Dict[str, str]] = core.get_file_history(
            self.json_data,
        )
        self.file_version: str = core.get_file_version(self.json_data)
        self.frew_version: str = core.get_frew_version(self.json_data)
        self.num_stages: int = core.get_num_stages(self.json_data)
        self.stage_names: List[str] = core.get_stage_names(
            self.json_data,
            self.num_stages,
        )
        self.num_nodes: int = core.get_num_nodes(
            self.json_data,
            self.num_stages,
        )

    # Soil based methods
    def get_materials(self) -> List[str]:
        """ Get the materials in the Frew model.

        Returns
        -------
        materials : List[str]
            A names of the materials in the Frew model.

        """
        return soil.get_materials(self.json_data)

    # Wall based methods
    def get_node_levels(self) -> List[float]:
        """ Get the levels of each node in the Frew model.

        Returns
        -------
        node_levels : List[float]
            The levels of each node in the Frew model.

        """
        return wall.get_node_levels(
            self.json_data,
            self.num_nodes,
        )

    def get_results(self) -> Dict[int, dict]:
        """ Get the shear, bending moment and displacement of the wall for each
        stage, node and design case.

        Returns
        -------
        wall_results : Dict[int, dict]
            The shear, bending and displacement results of the wall.

        """
        return wall.get_results(
            self.json_data,
            self.num_nodes,
            self.num_stages,
        )

    def results_to_excel(self) -> None:
        """ Export the wall results to an excel file where each worksheet is a
        design case. The spreadsheet will be output to the same folder as the
        models with the suffix '_results'.

        Returns
        -------
        None

        """
        wall_results = wall.get_results(
            self.json_data,
            self.num_nodes,
            self.num_stages,
        )
        node_levels = wall.get_node_levels(
            self.json_data,
            self.num_nodes,
        )
        return wall.results_to_excel(
            self.file_path,
            node_levels,
            wall_results,
            self.num_nodes,
            self.num_stages,
        )
