import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pltexp


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
