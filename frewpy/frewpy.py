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

    Attributes
    ----------
    wall : Class
        All wall related methods.
    struts : Class
        All strut related methods.
    soil : Class
        All soil related methods.
    water : Class
        All water related methods.

    """
    def __init__(self, file_path):
        self.model = win32com.client.Dispatch("frewLib.FrewComAuto")
        self.file_path = file_path
        self.folder_path = os.path.dirname(self.file_path)
        self.model.Open(self.file_path)
        self.model.DeleteResults()

        # Initialise sub-classes as attributes of main model object
        self.wall = _Wall(self.model, self.file_path, self.folder_path)
        self.struts = _Struts(self.model, self.file_path, self.folder_path)
        self.soil = _Soil(self.model, self.file_path, self.folder_path)
        self.water = _Water(self.model, self.file_path, self.folder_path)

    def analyse(self):
        self.model.GetNumStages()
        self.model.Analyse(self.model.GetNumStages()-1)

    def close(self):
        self.model.Close()


class _Wall():
    """ A class to get and set information relating to wall nodes.

    ...

    Methods
    -------
    get_num_nodes()
    get_node_levels()

    Attributes
    ----------


    """

    def __init__(self, model, file_path, folder_path):
        self.model = model
        self.file_path = file_path
        self.folder_path = folder_path
        self.num_nodes = self.get_num_nodes()
        self.num_stages = self.get_num_stages()

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

    def get_node_levels(self) -> dict:
        """ Function to get the levels of the nodes in a Frew model.

        Returns
        -------
        node_levels : dict
            The levels of each node in a Frew model.

        """
        node_levels = {}
        for node in range(0, self.get_num_nodes()):
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
                wall_results[stage+1] = {}
                for node in range(0, self.num_nodes):
                    wall_results[stage+1][node+1] = [
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
            wall_stiffness[stage+1] = {}
            for node in range(0, self.num_nodes):
                wall_stiffness[stage+1][node+1] = self.model.GetWallEI(
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
                'shear': [],
                'bending': [],
                'disp': []
            }

        for node in range(0, self.num_nodes):
            shear = []
            bending = []
            disp = []

            for stage in range(0, self.num_stages):
                shear.append(wall_results[stage+1][node+1][0])
                bending.append(wall_results[stage+1][node+1][1])
                disp.append(wall_results[stage+1][node+1][2])

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
            figure_title = f'{file_name} - Stage {stage+1}'

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
            for val in wall_results[stage+1].values():
                shear.append(val[0])
                bending.append(val[1])
                disp.append(val[2])

            # Plot for shear
            ax1.set_xlabel('Shear (kN/m)')
            ax1.set_ylabel('Level (m)')
            ax1.grid(color='#c5c5c5', linewidth=0.5)
            ax1.plot(envelopes['maximum']['shear'], levels, 'k--')
            ax1.plot(envelopes['minimum']['shear'], levels, 'k--')
            ax1.plot(shear, levels, 'g')

            # Plot for bending
            ax2.set_xlabel('Bending Moment (kNm/m)')
            ax2.grid(color='#c5c5c5', linewidth=0.5)
            ax2.plot(envelopes['maximum']['bending'], levels, 'k--')
            ax2.plot(envelopes['minimum']['bending'], levels, 'k--')
            ax2.plot(bending, levels, 'r')

            # Plot for displacements
            ax3.set_xlabel('Displacements (mm/m)')
            ax3.grid(color='#c5c5c5', linewidth=0.5)
            ax3.plot(envelopes['maximum']['disp'], levels, 'k--')
            ax3.plot(envelopes['minimum']['disp'], levels, 'k--')
            ax3.plot(disp, levels, 'b')

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

    Attributes
    ----------


    """

    def __init__(self, model, file_path, folder_path):
        self.model = model
        self.file_path = file_path
        self.folder_path = folder_path


class _Water():
    """ A class to get and set information relating to the water.

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
