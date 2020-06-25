class Water:
    def __init__(self, json_data):
        self.json_data = json_data

    # def get_water_pressures(self) -> dict:
    #     """ Function to get the pore water pressure for each stage and node.

    #     Returns
    #     -------
    #     water_pressures : dict
    #         The pore water pressures along the wall.

    #     """

    #     water_pressures = {
    #         'left': {},
    #         'right': {}
    #     }
    #     for stage in range(0, self.num_stages):
    #         for side in water_pressures:
    #             water_pressures[side][stage] = {}
    #     for stage in range(0, self.num_stages):
    #         for node in range(0, self.num_nodes):
    #             water_pressures['left'][stage][node+1] = (
    #                 self.model.GetNodePPLeft(node, stage)
    #             )
    #             water_pressures['right'][stage][node+1] = (
    #                 self.model.GetNodePPRight(node, stage)
    #             )
    #     return water_pressures
