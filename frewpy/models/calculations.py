from .wall import _Wall
from .soil import _Soil
from .water import _Water


class _Calculations(_Wall, _Soil, _Water):
    """ A class to combine subclasses so that calculations can be done.

    ...

    Methods
    -------

    Attributes
    ----------


    """

    def __init__(self, model, file_path, folder_path, num_nodes, num_stages):
        self.model = model
        self.file_path = file_path
        self.folder_path = folder_path
        self.num_nodes = num_nodes
        self.num_stages = num_stages

    def total_pressures(self) -> dict:
        """ Function to get the total pressures for left and right for each
        stage and node.

        Returns
        -------
        total_pressures : dict
            The total soil pressures.

        """

        soil_pressures = self.get_soil_pressures()
        water_pressures = self.get_water_pressures()

        horizontal_pressures = soil_pressures['horizontal_eff']

        total_pressures = {}
        for side in ['left', 'right']:
            total_pressures[side] = {}
            for stage in range(0, self.num_stages):
                total_pressures[side][stage] = {}
                for node in range(0, self.num_nodes):
                    total_pressures[side][stage][node+1] = (
                        horizontal_pressures[side][stage][node+1]
                        + water_pressures[side][stage][node+1]
                    )
        return total_pressures

    def net_total_pressures(self) -> dict:
        """ Function to get the net total pressures for each stage and node.

        Returns
        -------
        net_total_pressures : dict
            The net soil pressures.

        """
        total_pressures = self.total_pressures()

        net_total_pressures = {}
        for stage in range(0, self.num_stages):
            net_total_pressures[stage] = {}
            for node in range(0, self.num_nodes):
                net_total_pressures[stage][node+1] = (
                    total_pressures['left'][stage][node+1]
                    - total_pressures['right'][stage][node+1]
                )
        return net_total_pressures
