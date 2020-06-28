"""
plot
====

This module contains the plotting classes that are used throughout Frewpy.

"""
import os
from datetime import datetime
from typing import Dict, List
import re

import matplotlib.pyplot as plt  # type: ignore
import matplotlib.lines as mlines  # type: ignore
import colorcet as cc  # type: ignore
from bokeh.io import output_file, show, save  # type: ignore
from bokeh.layouts import layout  # type: ignore
from bokeh.plotting import figure  # type: ignore
from bokeh.models import (
    ColumnDataSource, CrosshairTool, HoverTool, Panel, Tabs
)  # type: ignore
from bokeh.models.widgets.markups import Div  # type: ignore


class FrewPlot:
    def __init__(self, titles: dict):
        self.fig_size = (11.69, 8.27)
        self.titles = titles

        self.title_size = 10
        self.label_size = 7
        self.x_labels = [
            "Bending Moment (kNm/m)",
            "Shear (kN/m)",
            "Displacements (mm)",
        ]
        self.y_labels = ["Level (m)", None, None]

        self.grid_colour = "#c5c5c5"
        self.grid_wid = 0.5
        self.line_wid = 1

        self.plot_types = ["bending", "shear", "disp"]

    def get_title(self, stage: int, stage_name: str, bokeh: bool = False):
        if bokeh:
            sep = "<br>"
        else:
            sep = "\n"

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
        fig_title += f"{sep} Stage {stage} - {stage_name}"

        return fig_title

    def get_data(self, wall_results: Dict[int, dict], stage) -> List[List]:
        bending = []
        shear = []
        disp = []
        for val in wall_results[stage].values():
            bending.append(val["bending"])
            shear.append(val["shear"])
            disp.append(val["displacement"])
        return [bending, shear, disp]


class FrewMPL(FrewPlot):
    def __init__(
        self,
        titles: dict,
        stage: int,
        stage_name: str,
        wall_results: Dict[int, dict],
        node_levels: List[float],
        envelopes: Dict[str, dict],
    ):
        super().__init__(titles)
        self.stage = stage
        self.stage_name = stage_name
        self.wall_results = wall_results
        self.node_levels = node_levels
        self.envelopes = envelopes

        self.cases = list(self.envelopes.keys())
        self.labels = ["Nodes", "Max Env", "Min Env", *self.cases]
        self.handles = []

        # Get data to plot
        plot_lists = self.get_data(self.wall_results, self.stage)
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
        for axis, plot_list, plot_type in zip(
            axes, plot_lists, self.plot_types
        ):
            result_handles = []
            for i, (case_data, color) in enumerate(zip(plot_list, colors)):
                # Plot results
                (res_handle,) = axis.plot(
                    case_data, self.node_levels, color=color
                )

                # Plot max envelope
                axis.plot(
                    envelopes[self.cases[i]]["maximum"][plot_type],
                    self.node_levels,
                    color=color,
                    linestyle="--",
                    linewidth=1,
                )

                # Plot min envelope
                axis.plot(
                    envelopes[self.cases[i]]["minimum"][plot_type],
                    self.node_levels,
                    color=color,
                    linestyle=":",
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
            mlines.Line2D([], [], color="gray", linestyle="--")
        )
        self.handles.append(
            mlines.Line2D([], [], color="gray", linestyle=":")
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


class FrewBokeh(FrewPlot):
    def __init__(
        self,
        file_name: str,
        titles: dict,
        num_stages: int,
        stage_names: List[str],
        wall_results: Dict[int, dict],
        node_levels: List[float],
        envelopes: Dict[str, dict]
    ):
        super().__init__(titles)
        self.file_name = file_name
        self.num_stages = num_stages
        self.stage_names = stage_names
        self.wall_results = wall_results
        self.node_levels = node_levels
        self.envelopes = envelopes

        self.cases = list(self.envelopes.keys())
        self.plot_wid = 500
        self.plot_hgt = 750
        self.tabs = []

        output_file(file_name)

        for stage in range(0, self.num_stages):
            stage_name = self.stage_names[stage]
            # Create the plot title
            fig_title = self.get_title(stage, stage_name, bokeh=True)
            title_div = Div(
                text=f"<h1>{fig_title}</h1>",
                style={
                    "color": "#fff",
                    "width": f"{self.plot_wid*3}px",
                    "font-size": "10px",
                    "background-color": "#222222",
                    "text-align": "center"
                },
            )

            # Get data to plot
            plot_lists = self.get_data(self.wall_results, stage)
            num_cases = len(self.cases)
            node_list = [i for i in range(1, len(self.node_levels) + 1)]
            colors = cc.glasbey[0:num_cases]

            # Create a list of 3 Bokeh figures
            self.figs = []
            for i in range(3):
                self.figs.append(
                    figure(
                        plot_width=self.plot_wid,
                        plot_height=self.plot_hgt,
                        title=None,
                        output_backend="webgl"
                    )
                )

            # Set up the plot properties
            for x_label, y_label, fig in zip(
                self.x_labels, self.y_labels, self.figs
            ):
                if y_label:
                    fig.yaxis.axis_label = y_label
                if x_label:
                    fig.xaxis.axis_label = x_label

                # Manipulate strings to create hovertool information
                if not y_label:
                    y_label = "Level (m)"

                x_info = re.sub(r"\(.+\)", "", x_label)
                y_info = re.sub(r"\(.+\)", "", y_label)
                x_unit = re.findall(r"\(([^)]+)\)", x_label)[0]
                y_unit = re.findall(r"\(([^)]+)\)", y_label)[0]

                ht = HoverTool()
                ht.tooltips = [
                    (f"{x_info}", "$x{0.2f} " + x_unit),
                    (f"{y_info}", "$y{0.2f} " + y_unit),
                ]
                fig.add_tools(ht)
                fig.add_tools(CrosshairTool())

            # Plot values
            node_source = ColumnDataSource(
                {
                    "xs": [0] * len(self.node_levels),
                    "ys": self.node_levels,
                    "node_num": node_list
                }
            )
            for fig, plot_list, plot_type in zip(
                self.figs, plot_lists, self.plot_types
            ):
                for i, (case_data, color) in enumerate(zip(plot_list, colors)):
                    # Plot node geometry
                    fig.circle(
                        x="xs",
                        y="ys",
                        size=7.5,
                        color="gray",
                        alpha=0.1,
                        source=node_source,
                        legend_label="Nodes"
                    )

                    # Plot results
                    res_source = ColumnDataSource(
                        {
                            "xs": case_data,
                            "ys": self.node_levels,
                            "node_num": node_list
                        }
                    )
                    fig.line(
                        x="xs",
                        y="ys",
                        color=color,
                        source=res_source,
                        legend_label=self.cases[i]
                    )
                    fig.circle(
                        x="xs",
                        y="ys",
                        size=3,
                        color=color,
                        source=res_source,
                        legend_label=self.cases[i]
                    )

                fig.legend.click_policy = "hide"
                fig.legend.location = "bottom_right"

            lay = layout([[title_div], [[self.figs]]])
            self.tabs.append(
                Panel(child=lay, title=f"Stage {stage}")
            )
        show(Tabs(tabs=self.tabs))
