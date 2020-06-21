from .exceptions import FrewError


def get_materials(json_data: dict) -> list:
    """ Gets a list of materials present in the Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.

    Returns
    -------
    materials : list
        A list of the materials in the Frew model.

    """
    if not json_data.get('Materials', False):
        raise FrewError('No materials defined in the model')
    return [material_dict['Name'] for material_dict in json_data['Materials']]


def get_material_properties():
    pass

# def get_material_properties(json_data: dict, material: str) -> dict:
#     """ Method to return all the properties of a specific material.

#     Parameters
#     ----------
#     material : str
#         The name of the material to return the properties for.

#     Returns
#     -------
#     material_properties : dict
#         A sentence explaining what the variable is.

#     """

#     if not type(material) == str:
#         raise FrewError('Input material must be a string.')
#     if not json_data.get('Materials', False):
#         raise FrewError('No materials defined in the model')
#     material_properties = False
#     for material_dict in json_data['Materials']:
#         if material_dict['Name'] == material:
#             material_properties = material_dict
#     if not material_properties:
#         raise FrewError(f'No material called {material} in the model.')
#     return material_properties


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
