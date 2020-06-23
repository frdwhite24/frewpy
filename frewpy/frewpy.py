"""
frewpy
======

This module is a python wrapper for Oasys Frew, an embedded retaining wall
engineering design software.

"""

import os
import json

from typing import Dict, List, Union

from frewpy.models import soil, core, wall, struts
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

    Methods
    -------
    get_materials() -> List[str]
        Get names of all the materials used within the Frew model.
    get_material_properties(material: str) -> Dict[str, Union[float, int, dict, bool]]
        Get the properties of a material in the Frew model.
    get_node_levels() -> List[float]
        Get the levels of each node in the Frew model.
    get_results() -> Dict[int, dict]
        Get the shear, bending moment and displacement of the wall for each
        stage, node and design case.
    results_to_excel() -> None
        Export the wall results to an excel file where each worksheet is a
        design case. The spreadsheet will be output to the same folder as the
        models with the suffix '_results'.

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
            self.json_data, self.num_stages,
        )
        self.num_nodes: int = core.get_num_nodes(
            self.json_data, self.num_stages,
        )

    # Soil based methods
    def get_materials(self) -> List[str]:
        """ Get names of all the materials used within the Frew model.

        Returns
        -------
        materials : List[str]
            The names of the materials in the Frew model.

        """
        return soil.get_materials(self.json_data)

    def get_material_properties(
        self, material: str
    ) -> Dict[str, Union[float, int, dict, bool]]:
        """ Get the properties of a material in the Frew model.

        Returns
        -------
        material_properties : Dict[str, Union[float, int, dict, bool]]
            The properties of the input material.

        """
        return soil.get_material_properties(self.json_data, material)

    # Wall based methods
    def get_node_levels(self) -> List[float]:
        """ Get the levels of each node in the Frew model.

        Returns
        -------
        node_levels : List[float]
            The levels of each node in the Frew model.

        """
        return wall.get_node_levels(self.json_data, self.num_nodes,)

    def get_results(self) -> Dict[int, dict]:
        """ Get the shear, bending moment and displacement of the wall for each
        stage, node and design case.

        Returns
        -------
        wall_results : Dict[int, dict]
            The shear, bending and displacement results of the wall.

        """
        return wall.get_results(
            self.json_data, self.num_nodes, self.num_stages,
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
            self.json_data, self.num_nodes, self.num_stages,
        )
        node_levels = wall.get_node_levels(self.json_data, self.num_nodes,)
        return wall.results_to_excel(
            self.file_path,
            node_levels,
            wall_results,
            self.num_nodes,
            self.num_stages,
        )

    # Strut based methods
    def get_struts(self) -> List[dict]:
        """ Get a list of all the strut objects within the Frew model.

        Returns
        -------
        struts : List[dict]
            A list of struts in the Frew model.

        """
        return struts.get_struts(self.json_data)

    def get_strut_by_node(
        self, node: int
    ) -> Dict[str, Union[float, int, bool]]:
        """ Get a strut object at the specified node location within the Frew
        model. If more than one strut is found, the first strut occurence is
        returned.

        Parameters
        ----------
        node : int
            The node number of the strut

        Returns
        -------
        strut : Dict[str, Union[float, int, bool]]
            A strut object represented as a dictionary in the Frew model
            matching the input node number.

        """
        return struts.get_strut_by_node(self.json_data, node)

    def get_struts_by_node(self, node: int) -> List[dict]:
        """ Get a list of strut objects at the specified node location within
        the Frew model.

        Parameters
        ----------
        node : int
            The node number of the strut

        Returns
        -------
        struts : Dict[str, Union[float, int, bool]]
            A list of struts in the Frew model that match the input node
            number.

        """
        return struts.get_struts_by_node(self.json_data, node)
