"""
plot
====

This module contains the plotting classes that are used throughout Frewpy.

"""
import os
from datetime import datetime
from typing import Dict, List

import matplotlib.pyplot as plt  # type: ignore
import matplotlib.backends.backend_pdf as pltexp  # type: ignore
import matplotlib.lines as mlines  # type: ignore
import colorcet as cc  # type: ignore


class FrewPlot():
    def __init__(self, titles: dict):
        self.fig_size = (11.69, 8.27)
        self.titles = titles

        self.title_size = 10
        self.label_size = 7
        self.x_labels = [
            "Displacements (mm)",
            "Bending Moment (kNm/m)",
            "Shear (kN/m)"
        ]
        self.y_labels = ["Level (m)", None, None]

        self.grid_colour = "#c5c5c5"
        self.grid_wid = 0.5
        self.line_wid = 1

    def get_title(self, stage: int, stage_name: str):
        fig_title = self.titles["JobTitle"]

        if self.titles.get("Subtitle", False):
            fig_title += f" , {self.titles['Subtitle']}"
        if self.titles.get("CalculationHeading", False):
            fig_title += f"\n{self.titles['CalculationHeading']}"
        if self.titles.get("JobNumber", False):
            fig_title += f"\n Job num: {self.titles['JobNumber']}"
        if self.titles.get("Initials", False):
            fig_title += f", Designed by: {self.titles['Initials']}"

        fig_title += f", Date: {datetime.now().strftime(r'%d/%m/%Y')}"
        fig_title += f"\n Stage {stage} - {stage_name}"

        return fig_title


class FrewMPL(FrewPlot):
    def __init__(
        self,
        titles: dict,
        stage: int,
        stage_name: str,
        wall_results: Dict[int, dict],
        node_levels: List[float],
        envelopes: list
    ):
        super().__init__(titles)
        self.stage = stage
        self.stage_name = stage_name
        self.wall_results = wall_results
        self.node_levels = node_levels
        self.envelopes = envelopes

        self.cases = list(self.envelopes.keys())
        self.labels = ["Nodes", "Max Env", "Min Env"]
        self.labels.extend(self.cases)
        self.handles = []

        # Get data to plot
        shear = []
        bending = []
        disp = []
        for val in self.wall_results[self.stage].values():
            shear.append(val["shear"])
            bending.append(val["bending"])
            disp.append(val["displacement"])
        plot_lists = [bending, shear, disp]
        plot_types = ["bending", "shear", "disp"]

        num_cases = len(self.cases)
        colors = cc.glasbey[0:num_cases]

        # Create figure with subplots
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(
            1, 3, sharey=True, figsize=self.fig_size
        )
        axes = [self.ax1, self.ax2, self.ax3]

        # Create and set the plot title
        fig_title = self.get_title(self.stage, self.stage_name)
        self.fig.suptitle(fig_title, fontsize=self.title_size)

        # Set up the plot properties
        for x_label, y_label, axis in zip(self.x_labels, self.y_labels, axes):
            axis.tick_params(labelsize=self.label_size)
            axis.grid(color=self.grid_colour, linewidth=self.grid_wid)
            if y_label:
                axis.set_ylabel(y_label, fontsize=self.label_size)
            if x_label:
                axis.set_xlabel(x_label, fontsize=self.label_size)

        # Plot values
        for axis, plot_list, plot_type in zip(axes, plot_lists, plot_types):
            result_handles = []
            for i, (case_data, color) in enumerate(zip(plot_list, colors)):
                # Plot results
                (res_handle,) = axis.plot(
                    case_data,
                    self.node_levels,
                    color=color
                )

                # Plot max envelope
                axis.plot(
                    envelopes[self.cases[i]]['maximum'][plot_type],
                    self.node_levels,
                    color=color,
                    linestyle='--',
                    linewidth=1,
                )

                # Plot min envelope
                axis.plot(
                    envelopes[self.cases[i]]['minimum'][plot_type],
                    self.node_levels,
                    color=color,
                    linestyle=':',
                    linewidth=1,
                )

                # Plot node geometry
                (node_handle,) = axis.plot(
                    [0] * len(self.node_levels),
                    self.node_levels,
                    marker=".",
                    ls="",
                    alpha=0.1,
                    color="0.5",
                    rasterized=True,
                )
                result_handles.append(res_handle)

        # Construct handle for legend.
        self.handles = [node_handle]
        self.handles.append(
            mlines.Line2D([], [], color='gray', linestyle='--')
        )
        self.handles.append(
            mlines.Line2D([], [], color='gray', linestyle=':')
        )
        self.handles.extend(result_handles)

        self.fig.legend(
            self.handles,
            self.labels,
            loc="lower center",
            bbox_to_anchor=(0.5, 0.02),
            ncol=10,
            fontsize=self.label_size,
        )
