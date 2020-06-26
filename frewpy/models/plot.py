"""
plot
====

This module contains the plotting classes that are used throughout Frewpy.

"""
import os

import matplotlib.pyplot as plt  # type: ignore
import matplotlib.backends.backend_pdf as pltexp  # type: ignore


class FrewPlot():
    def __init__(self):
        self.title_size = 10
        self.label_size = 7
        self.x_labels = [
            "Displacements (mm/m)",
            "Bending Moment (kNm/m)",
            "Shear (kN/m)"
        ]
        self.y_labels = ["Level (m)", None, None]

        self.grid_col = "#c5c5c5"
        self.grid_wid = 0.5

        self.line_wid = 1
        self.line_style = "k--"


class FrewMPL(FrewPlot):
    def __init__(
        self,
        file_name: str,
        stage: int,
        wall_results: list,
        node_levels: list,
        envelopes: list
    ):
        super().__init__()
        self.file_name = file_name
        self.stage = stage
        self.wall_results = wall_results
        self.node_levels = node_levels
        self.envelopes = envelopes

        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(
            1, 3, sharey=True
        )
        self.fig_title = f'{file_name} - Stage {stage}'
        self.fig.suptitle(self.fig_title)

        axes = [self.ax1, self.ax2, self.ax3]
        for x_label, y_label, axis in zip(self.x_labels, self.y_labels, axes):
            if y_label:
                axis.set_ylabel(y_label)
                axis.set_yticklabels(fontsize=self.label_size)
            if x_label:
                axis.set_xlabel(x_label)
                axis.set_xticklabels(fontsize=self.label_size)

        plt.show()

# def plot_results() -> None:

#     # Set defaults for plot styling
#     plt.rcParams.update({'axes.titlesize': 10})
#     plt.rcParams.update({'axes.labelsize': 7})
#     plt.rcParams.update({'xtick.labelsize': 7})
#     plt.rcParams.update({'ytick.labelsize': 7})

#     pdf = pltexp.PdfPages(
#         f'{os.path.join(folder_path, file_name)}_results.pdf'
#     )
#     for stage in range(0, num_stages):
#         # Data to plot
#         levels = []
#         shear = []
#         bending = []
#         disp = []
#         for level in node_levels.values():
#             levels.append(level)
#         for val in wall_results[stage].values():
#             shear.append(val[0])
#             bending.append(val[1])
#             disp.append(val[2])

#         # Plot for displacements
#         ax1.set_xlabel('Displacements (mm/m)')
#         ax1.set_ylabel('Level (m)')
#         ax1.grid(color='#c5c5c5', linewidth=0.5)
#         ax1.plot(
#             envelopes['maximum']['disp'],
#             levels,
#             'k--',
#             linewidth=1
#         )
#         ax1.plot(
#             envelopes['minimum']['disp'],
#             levels,
#             'k--',
#             linewidth=1
#         )
#         ax1.plot(disp, levels, 'b')

#         # Plot for bending
#         ax2.set_xlabel('Bending Moment (kNm/m)')
#         ax2.grid(color='#c5c5c5', linewidth=0.5)
#         ax2.plot(
#             envelopes['maximum']['bending'],
#             levels,
#             'k--',
#             linewidth=1
#         )
#         ax2.plot(
#             envelopes['minimum']['bending'],
#             levels,
#             'k--',
#             linewidth=1
#         )
#         ax2.plot(bending, levels, 'r')

#         # Plot for shear
#         ax3.set_xlabel('Shear (kN/m)')
#         ax3.grid(color='#c5c5c5', linewidth=0.5)
#         ax3.plot(
#             envelopes['maximum']['shear'],
#             levels,
#             'k--',
#             linewidth=1
#         )
#         ax3.plot(
#             envelopes['minimum']['shear'],
#             levels,
#             'k--',
#             linewidth=1
#         )
#         ax3.plot(shear, levels, 'g')

#         pdf.savefig(fig)
#     pdf.close()