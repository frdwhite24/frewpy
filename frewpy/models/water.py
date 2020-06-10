class _Water():
    """ A class to get and set information relating to the water.

    ...

    Methods
    -------
    get_water_pressures()

    Attributes
    ----------


    """

    def __init__(self, model, file_path, folder_path, num_nodes, num_stages):
        self.model = model
        self.file_path = file_path
        self.folder_path = folder_path
        self.num_nodes = num_nodes
        self.num_stages = num_stages

    def get_water_pressures(self) -> dict:
        """ Function to get the pore water pressure for each stage and node.

        Returns
        -------
        water_pressures : dict
            The pore water pressures along the wall.

        """

        water_pressures = {
            'left': {},
            'right': {}
        }
        for stage in range(0, self.num_stages):
            for side in water_pressures:
                water_pressures[side][stage] = {}
        for stage in range(0, self.num_stages):
            for node in range(0, self.num_nodes):
                water_pressures['left'][stage][node+1] = (
                    self.model.GetNodePPLeft(node, stage)
                )
                water_pressures['right'][stage][node+1] = (
                    self.model.GetNodePPRight(node, stage)
                )
        return water_pressures
