class Calculation:
    def __init__(self, json_data):
        self.json_data = json_data

    # def total_pressures(self) -> dict:
    #     """ Function to get the total pressures for left and right for each
    #     stage and node.

    #     Returns
    #     -------
    #     total_pressures : dict
    #         The total soil pressures.

    #     """

    #     soil_pressures = self.get_soil_pressures()
    #     water_pressures = self.get_water_pressures()

    #     horizontal_pressures = soil_pressures['horizontal_eff']

    #     total_pressures = {}
    #     for side in ['left', 'right']:
    #         total_pressures[side] = {}
    #         for stage in range(0, self.num_stages):
    #             total_pressures[side][stage] = {}
    #             for node in range(0, self.num_nodes):
    #                 total_pressures[side][stage][node+1] = (
    #                     horizontal_pressures[side][stage][node+1]
    #                     + water_pressures[side][stage][node+1]
    #                 )
    #     return total_pressures

    # def net_total_pressures(self) -> dict:
    #     """ Function to get the net total pressures for each stage and node.

    #     Returns
    #     -------
    #     net_total_pressures : dict
    #         The net soil pressures.

    #     """
    #     total_pressures = self.total_pressures()

    #     net_total_pressures = {}
    #     for stage in range(0, self.num_stages):
    #         net_total_pressures[stage] = {}
    #         for node in range(0, self.num_nodes):
    #             net_total_pressures[stage][node+1] = (
    #                 total_pressures['left'][stage][node+1]
    #                 - total_pressures['right'][stage][node+1]
    #             )
    #     return net_total_pressures
