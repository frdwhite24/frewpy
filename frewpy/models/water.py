"""
Water
=====

This module holds the class for the Water object.

"""

from typing import Dict, List

from frewpy.utils import (
    check_results_present,
    get_num_stages,
    get_num_nodes,
    get_design_case_names,
)


class Water:
    """ A class used to contain any water related functionality of frewpy.

    """

    def __init__(self, json_data):
        self.json_data = json_data

    def get_water_pressures(self) -> Dict[int, Dict[str, dict]]:
        """ Function to get the pore water pressure for each stage and node.

        Returns
        -------
        water_pressures : Dict[int, Dict[str, dict]]
            The pore water pressures along the wall.

        """
        check_results_present(self.json_data)
        num_nodes: int = get_num_nodes(self.json_data)
        num_stages: int = get_num_stages(self.json_data)
        design_cases: List[str] = get_design_case_names(self.json_data)

        water_pressures: Dict[int, Dict[str, dict]] = {}

        for stage in range(num_stages):
            water_pressures[stage] = {
                design_case: {"left": [], "right": [],}
                for design_case in design_cases
            }

        for index, design_case in enumerate(design_cases):
            for stage in range(num_stages):
                node_results = self.json_data["Frew Results"][index][
                    "Stageresults"
                ][stage]["Noderesults"]
                for node in range(num_nodes):
                    water_pressures[stage][design_case]["left"].append(
                        node_results[node]["ULeft"] / 1000
                    )
                    water_pressures[stage][design_case]["right"].append(
                        node_results[node]["URight"] / 1000
                    )
        return water_pressures
