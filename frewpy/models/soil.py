class _Soil():
    """ A class to get and set information relating to the soil.

    ...

    Methods
    -------
    get_soil_pressures()

    Attributes
    ----------


    """

    def __init__(self, model, file_path, folder_path, num_nodes, num_stages):
        self.model = model
        self.file_path = file_path
        self.folder_path = folder_path
        self.num_nodes = num_nodes
        self.num_stages = num_stages

    def get_soil_pressures(self) -> dict:
        """ Function to get the vertical effective and horizontal effective for
        each stage and node.

        Returns
        -------
        soil_pressures : dict
            The vertical effective and horizontal effective soil pressures.

        """

        soil_pressures = {
            'vertical_eff': {},
            'horizontal_eff': {}
        }
        for stress_type in soil_pressures:
            soil_pressures[stress_type]['left'] = {}
            soil_pressures[stress_type]['right'] = {}
            for stage in range(0, self.num_stages):
                for side in soil_pressures[stress_type]:
                    soil_pressures[stress_type][side][stage] = {}
        for stage in range(0, self.num_stages):
            for node in range(0, self.num_nodes):
                soil_pressures['horizontal_eff']['left'][stage][node+1] = (
                    self.model.GetNodePeLeft(node, stage)
                )
                soil_pressures['horizontal_eff']['right'][stage][node+1] = (
                    self.model.GetNodePeRight(node, stage)
                )
                soil_pressures['vertical_eff']['left'][stage][node+1] = (
                    self.model.GetNodeVeLeft(node, stage)
                )
                soil_pressures['vertical_eff']['right'][stage][node+1] = (
                    self.model.GetNodeVeRight(node, stage)
                )
        return soil_pressures
