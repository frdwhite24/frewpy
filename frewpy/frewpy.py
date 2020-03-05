"""
frewpy
======

This module is a python wrapper for Oasys Frew, an embedded retaining wall
engineering design software.

"""

from pprint import pprint
import os

import win32com.client
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pltexp


class FrewModel():
    """ A class used to establish a connection to any Frew model and to
    manipulate it as required using pythonic terms and OOP.

    ...

    Methods
    -------
    analyse()
        To run the analysis on a Frew model.
    close()
        To close the COM connection to a Frew model.
    get_num_nodes()
        To get the number of nodes in a Frew model.
    get_num_stages()
        To get the number of stages in a Frew model.

    Attributes
    ----------
    wall : FrewModel._Wall
        All wall related methods.
    struts : FrewModel._Struts
        All strut related methods.
    soil : FrewModel._Soil
        All soil related methods.
    water : FrewModel._Water
        All water related methods.

    """
    def __init__(self, file_path):
        self.model = win32com.client.Dispatch("frewLib.FrewComAuto")
        self.file_path = file_path
        self.folder_path = os.path.dirname(self.file_path)
        self.model.Open(self.file_path)
        self.model.DeleteResults()

        self.num_nodes = self.get_num_nodes()
        self.num_stages = self.get_num_stages()

        # Initialise sub-classes as attributes of main model object
        self.wall = _Wall(
            self.model,
            self.file_path,
            self.folder_path,
            self.num_nodes,
            self.num_stages
        )
        self.struts = _Struts(self.model, self.file_path, self.folder_path)
        self.soil = _Soil(
            self.model,
            self.file_path,
            self.folder_path,
            self.num_nodes,
            self.num_stages
        )
        self.water = _Water(
            self.model,
            self.file_path,
            self.folder_path,
            self.num_nodes,
            self.num_stages
        )
        self.calculate = _Calculations(
            self.model,
            self.file_path,
            self.folder_path,
            self.num_nodes,
            self.num_stages
        )

    def analyse(self):
        self.model.GetNumStages()
        self.model.Analyse(self.model.GetNumStages()-1)

    def close(self):
        self.model.Close()

    def get_num_nodes(self) -> int:
        """ Function to get the number of nodes in a Frew model.

        Returns
        -------
        num_nodes : int
            The number of nodes in a Frew model.

        """
        num_nodes = self.model.GetNumNodes()
        return num_nodes

    def get_num_stages(self) -> int:
        """ Function to get the number of stages in a Frew model.

        Returns
        -------
        num_stages : int
            The number of stages in a Frew model.

        """
        num_stages = self.model.GetNumStages()
        return num_stages


class FrewError(BaseException):
    def __init__(self):
        pass


class _Wall():
    """ A class to get and set information relating to wall nodes.

    ...

    Methods
    -------
    get_node_levels()

    Attributes
    ----------


    """

    def __init__(self, model, file_path, folder_path, num_nodes, num_stages):
        self.model = model
        self.file_path = file_path
        self.folder_path = folder_path
        self.num_nodes = num_nodes
        self.num_stages = num_stages

    def get_node_levels(self) -> dict:
        """ Function to get the levels of the nodes in a Frew model.

        Returns
        -------
        node_levels : dict
            The levels of each node in a Frew model.

        """
        node_levels = {}
        for node in range(0, self.num_nodes):
            node_levels[node+1] = self.model.GetNodeLevel(node)
        return node_levels

    def get_results(self) -> dict:
        """ Function to get the shear, bending moment and displacement of the
        wall for each stage and node.

        Returns
        -------
        wall_results : dict
            The shear, bending and displacement of the wall.

        """
        wall_results = {}
        try:
            for stage in range(0, self.num_stages):
                wall_results[stage] = {}
                for node in range(0, self.num_nodes):
                    wall_results[stage][node+1] = [
                        self.model.GetNodeShear(node, stage),
                        self.model.GetNodeBending(node, stage),
                        self.model.GetNodeDisp(node, stage)
                    ]
        except Exception as e:
            wall_results = {}
            print(
                'Error! No results in model, please analyse the model first.'
            )
        return wall_results

    def get_wall_stiffness(self) -> dict:
        """ Function to get the stiffness of the wall for each stage and node.

        Returns
        -------
        wall_stiffness : dict
            The stiffness of the wall.

        """
        wall_stiffness = {}
        for stage in range(0, self.num_stages):
            wall_stiffness[stage] = {}
            for node in range(0, self.num_nodes):
                wall_stiffness[stage][node+1] = self.model.GetWallEI(
                    node,
                    stage
                )
        return wall_stiffness

    def get_envelopes(self) -> dict:
        """ Function to return the envelopes of max and min shear, bending and
        displacements. 

        """

        wall_results = self.get_results()

        envelopes = {
            'maximum': {},
            'minimum': {}
        }
        for key in envelopes:
            envelopes[key] = {
                # change these lists into dictionaries with node numbers so
                # they are the same format as others
                'shear': [],
                'bending': [],
                'disp': []
            }

        for node in range(0, self.num_nodes):
            shear = []
            bending = []
            disp = []

            for stage in range(0, self.num_stages):
                shear.append(wall_results[stage][node+1][0])
                bending.append(wall_results[stage][node+1][1])
                disp.append(wall_results[stage][node+1][2])

            envelopes['maximum']['shear'].append(max(shear))
            envelopes['maximum']['bending'].append(max(bending))
            envelopes['maximum']['disp'].append(max(disp))
            envelopes['minimum']['shear'].append(min(shear))
            envelopes['minimum']['bending'].append(min(bending))
            envelopes['minimum']['disp'].append(min(disp))

        return envelopes

    def plot_results(self) -> None:
        """ Function to plot the shear, bending moment and displacement of the
        wall for each stage.

        """

        file_name = os.path.basename(self.file_path.rsplit('.', 1)[0])
        wall_results = self.get_results()
        node_levels = self.get_node_levels()
        envelopes = self.get_envelopes()

        # Set defaults for plot styling
        plt.rcParams.update({'axes.titlesize': 10})
        plt.rcParams.update({'axes.labelsize': 7})
        plt.rcParams.update({'xtick.labelsize': 7})
        plt.rcParams.update({'ytick.labelsize': 7})

        pdf = pltexp.PdfPages(
            f'{os.path.join(self.folder_path, file_name)}_results.pdf'
        )
        for stage in range(0, self.num_stages):
            figure_title = f'{file_name} - Stage {stage}'

            plt.close('all')
            fig, (ax1, ax2, ax3) = plt.subplots(
                1,
                3,
                sharey=True)

            # Figure information
            fig.suptitle(figure_title)

            # Data to plot
            levels = []
            shear = []
            bending = []
            disp = []
            for level in node_levels.values():
                levels.append(level)
            for val in wall_results[stage].values():
                shear.append(val[0])
                bending.append(val[1])
                disp.append(val[2])

            # Plot for displacements
            ax1.set_xlabel('Displacements (mm/m)')
            ax1.set_ylabel('Level (m)')
            ax1.grid(color='#c5c5c5', linewidth=0.5)
            ax1.plot(
                envelopes['maximum']['disp'],
                levels,
                'k--',
                linewidth=1
            )
            ax1.plot(
                envelopes['minimum']['disp'],
                levels,
                'k--',
                linewidth=1
            )
            ax1.plot(disp, levels, 'b')

            # Plot for bending
            ax2.set_xlabel('Bending Moment (kNm/m)')
            ax2.grid(color='#c5c5c5', linewidth=0.5)
            ax2.plot(
                envelopes['maximum']['bending'],
                levels,
                'k--',
                linewidth=1
            )
            ax2.plot(
                envelopes['minimum']['bending'],
                levels,
                'k--',
                linewidth=1
            )
            ax2.plot(bending, levels, 'r')

            # Plot for shear
            ax3.set_xlabel('Shear (kN/m)')
            ax3.grid(color='#c5c5c5', linewidth=0.5)
            ax3.plot(
                envelopes['maximum']['shear'],
                levels,
                'k--',
                linewidth=1
            )
            ax3.plot(
                envelopes['minimum']['shear'],
                levels,
                'k--',
                linewidth=1
            )
            ax3.plot(shear, levels, 'g')

            pdf.savefig(fig)
        pdf.close()


class _Struts():
    """ A class to get and set information relating to struts.

    ...

    Methods
    -------

    Attributes
    ----------


    """

    def __init__(self, model, file_path, folder_path):
        self.model = model
        self.file_path = file_path
        self.folder_path = folder_path


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


