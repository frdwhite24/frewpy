import json
import os
from typing import Dict, List, Union

from .exceptions import FrewError


class Strut:
    def __init__(self, json_data):
        self.json_data = json_data

    def _check_json_data(self):
        if not self.json_data.get("Struts", False):
            raise FrewError("No struts defined in the model")

    @staticmethod
    def _check_node_input_type(node: int):
        if type(node) != int:
            raise FrewError("Input node must be an integer.")

    def get_struts(self) -> List[dict]:
        """ Get a list of all the strut objects within the Frew model.

        Returns
        -------
        struts : List[dict]
            A list of struts in the Frew model.

        """
        self._check_json_data()
        return self.json_data["Struts"]

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
        self._check_node_input_type(node)
        self._check_json_data()

        for strut in self.get_struts():
            if strut["NodeStrut"] == node:
                return strut

        raise FrewError(
            f"There is no strut defined at node {node} in the model"
        )

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
        self._check_node_input_type(node)
        self._check_json_data()

        struts = [
            strut for strut in self.get_struts() if strut["NodeStrut"] == node
        ]
        if struts:
            return struts
        else:
            raise FrewError(
                f"There are no struts defined at node {node} in the model"
            )
