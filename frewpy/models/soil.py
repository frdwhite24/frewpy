from typing import List, Dict, Union

from .exceptions import FrewError


class Soil:
    """ A class used to contain any soil related functionality of frewpy.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    get_materials() -> List[str]
        Get names of all the materials used within the Frew model.
    get_material_properties(material: str) -> Dict[str, Union[float, int, dict, bool]]
        Get the properties of a material in the Frew model.

    """
    def __init__(self, json_data):
        self.json_data = json_data

    def get_materials(self) -> List[str]:
        """ Method to get names of all the materials used within the Frew
        model.

        Returns
        -------
        materials : List[str]
            A list of the materials in the Frew model.

        """
        if not self.json_data.get('Materials', False):
            raise FrewError('No materials defined in the model')
        return [
            material_dict['Name'] for material_dict in self.json_data[
                'Materials'
            ]
        ]

    def get_material_properties(
        self, material: str
    ) -> Dict[str, Union[float, int, dict, bool]]:
        """ Method to get all the properties of a specific material.

        Parameters
        ----------
        material : str
            The name of the material to return the properties for.

        Returns
        -------
        material_properties : Dict[str, Union[float, int, dict, bool]]
            The properties of the input material.

        """

        if type(material) != str:
            raise FrewError('Input material must be a string.')
        if not self.json_data.get('Materials', False):
            raise FrewError('No materials defined in the model')
        for material_dict in self.json_data['Materials']:
            if material_dict['Name'] == material:
                return material_dict
        raise FrewError(f'No material called {material} in the model.')


# def get_soil_pressures(self) -> dict:
#     """ Function to get the vertical effective and horizontal effective for
#     each stage and node.

#     Returns
#     -------
#     soil_pressures : dict
#         The vertical effective and horizontal effective soil pressures.

#     """

#     soil_pressures = {
#         'vertical_eff': {},
#         'horizontal_eff': {}
#     }
#     for stress_type in soil_pressures:
#         soil_pressures[stress_type]['left'] = {}
#         soil_pressures[stress_type]['right'] = {}
#         for stage in range(0, self.num_stages):
#             for side in soil_pressures[stress_type]:
#                 soil_pressures[stress_type][side][stage] = {}
#     for stage in range(0, self.num_stages):
#         for node in range(0, self.num_nodes):
#             soil_pressures['horizontal_eff']['left'][stage][node+1] = (
#                 self.model.GetNodePeLeft(node, stage)
#             )
#             soil_pressures['horizontal_eff']['right'][stage][node+1] = (
#                 self.model.GetNodePeRight(node, stage)
#             )
#             soil_pressures['vertical_eff']['left'][stage][node+1] = (
#                 self.model.GetNodeVeLeft(node, stage)
#             )
#             soil_pressures['vertical_eff']['right'][stage][node+1] = (
#                 self.model.GetNodeVeRight(node, stage)
#             )
#     return soil_pressures
