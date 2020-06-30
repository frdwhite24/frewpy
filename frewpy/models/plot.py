"""
Plot
====

This module contains the plotting classes that are used throughout Frewpy.

"""

from datetime import datetime
from typing import Dict, List, Tuple, Union
import re

import matplotlib.pyplot as plt  # type: ignore
import matplotlib.lines as mlines  # type: ignore
import colorcet as cc  # type: ignore
from bokeh.io import output_file, show  # type: ignore
from bokeh.layouts import layout  # type: ignore
from bokeh.plotting import figure  # type: ignore
from bokeh.models import (  # type: ignore
    ColumnDataSource,
    CrosshairTool,
    HoverTool,
    Panel,
    Tabs,
)
from bokeh.models.widgets.markups import Div  # type: ignore


class FrewPlot:
    def __init__(self, titles: Dict[str, str]) -> None:
        self.fig_size: Tuple[float, float] = (11.69, 8.27)
        self.titles: Dict[str, str] = titles

        self.title_size: int = 10
        self.label_size: int = 7
        self.x_labels: List[str] = [
            "Displacements (mm)",
            "Bending Moment (kNm/m)",
            "Shear (kN/m)",
        ]
        self.y_labels: List[Union[str, None]] = ["Level (m)", None, None]

        self.grid_colour: str = "#c5c5c5"
        self.grid_wid: float = 0.5
        self.line_wid: int = 1

        self.plot_types: List[str] = ["disp", "bending", "shear"]

    def get_title(
        self, stage: int, stage_name: str, bokeh: bool = False
    ) -> str:
        sep: str = "<br>" if bokeh else "\n"
        fig_title: str = self.titles["JobTitle"]

        if self.titles.get("Subtitle", False):
            fig_title += f" , {self.titles['Subtitle']}"
        if self.titles.get("CalculationHeading", False):
            fig_title += f"{sep}{self.titles['CalculationHeading']}"
        if self.titles.get("JobNumber", False):
            fig_title += f"{sep} Job num: {self.titles['JobNumber']}"
        if self.titles.get("Initials", False):
            fig_title += f", Designed by: {self.titles['Initials']}"

        fig_title += f", Date: {datetime.now().strftime(r'%d/%m/%Y')}"
        fig_title += f"{sep} Stage {stage} - {stage_name}"

        return fig_title

    def get_data(
        self, wall_results: Dict[int, dict], stage: int
    ) -> List[List[float]]:
        bending = []
        shear = []
        disp = []
        for val in wall_results[stage].values():
            bending.append(val["bending"])
            shear.append(val["shear"])
            disp.append(val["displacement"])
        return [disp, bending, shear]


class FrewMPL(FrewPlot):
    def __init__(
        self,
        titles: Dict[str, str],
        stage: int,
        stage_name: str,
        wall_results: Dict[int, dict],
        node_levels: List[float],
        envelopes: Dict[str, dict],
    ) -> None:
        super().__init__(titles)
        self.stage = stage
        self.stage_name = stage_name
        self.wall_results = wall_results
        self.node_levels = node_levels
        self.envelopes = envelopes

        self.cases: List[str] = list(self.envelopes.keys())
        self.labels = ["Nodes", "Envelope", *self.cases]
        self.handles = []

        # Get data to plot
        plot_lists = self.get_data(self.wall_results, self.stage)
        num_cases = len(self.cases)
        colors = cc.glasbey_bw[0:num_cases]

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
                # Plot node geometry
                (node_handle,) = axis.plot(
                    [0] * len(self.node_levels),
                    self.node_levels,
                    marker=".",
                    color="black",
                    alpha=0.5,
                )

                # Plot results
                (res_handle,) = axis.plot(
                    case_data, self.node_levels, color=color
                )

                # Plot max envelope
                axis.plot(
                    self.envelopes[self.cases[i]]["maximum"][plot_type],
                    self.node_levels,
                    color=color,
                    linestyle="--",
                    linewidth=1,
                )

                # Plot min envelope
                axis.plot(
                    self.envelopes[self.cases[i]]["minimum"][plot_type],
                    self.node_levels,
                    color=color,
                    linestyle="--",
                    linewidth=1,
                )

                result_handles.append(res_handle)

        # Construct handle for legend.
        self.handles = [node_handle]
        self.handles.append(
            mlines.Line2D([], [], color="gray", linestyle="--")
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
        envelopes: Dict[str, dict],
    ):
        super().__init__(titles)
        self.file_name = file_name
        self.num_stages = num_stages
        self.stage_names = stage_names
        self.wall_results = wall_results
        self.node_levels = node_levels
        self.envelopes = envelopes

        self.cases = list(self.envelopes.keys())
        self.plot_wid: int = 500
        self.plot_hgt: int = 750
        self.tabs: list = []

    def plot(self):
        output_file(self.file_name, title=self.titles["JobTitle"])
        for stage in range(self.num_stages):
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
                    "text-align": "center",
                },
            )

            # Get data to plot
            plot_lists = self.get_data(self.wall_results, stage)
            num_cases: int = len(self.cases)
            node_list: List[int] = list(range(1, len(self.node_levels) + 1))
            colors = cc.palette["glasbey_bw"][0:num_cases]

            # Create a list of 3 Bokeh figures
            self.figs = []
            for _ in range(3):
                self.figs.append(
                    figure(
                        plot_width=self.plot_wid, plot_height=self.plot_hgt,
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
                    ("Name", "$name"),
                    ("Node", "@node_num"),
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
                    "node_num": node_list,
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
                        size=3.5,
                        color="black",
                        alpha=0.5,
                        source=node_source,
                        legend_label="Wall",
                        name="Wall",
                    )
                    fig.line(
                        x="xs",
                        y="ys",
                        color="black",
                        source=node_source,
                        legend_label="Wall",
                        name="Wall",
                        line_width=2,
                    )

                    # Plot results
                    res_source = ColumnDataSource(
                        {
                            "xs": case_data,
                            "ys": self.node_levels,
                            "node_num": node_list,
                        }
                    )
                    fig.line(
                        x="xs",
                        y="ys",
                        color=color,
                        source=res_source,
                        legend_label=self.cases[i],
                        name=self.cases[i],
                        line_width=2,
                    )

                    # Plot max envelope
                    max_evenlope_xs = self.envelopes[self.cases[i]]["maximum"][
                        plot_type
                    ]
                    max_source = ColumnDataSource(
                        {
                            "xs": max_evenlope_xs,
                            "ys": self.node_levels,
                            "node_num": node_list,
                        }
                    )
                    fig.line(
                        x="xs",
                        y="ys",
                        color=color,
                        line_dash="dashed",
                        source=max_source,
                        legend_label=f"{self.cases[i]} envelope",
                        name=f"{self.cases[i]} envelope",
                        line_width=2,
                    )

                    # Plot min envelope
                    min_evenlope_xs = self.envelopes[self.cases[i]]["minimum"][
                        plot_type
                    ]
                    min_source = ColumnDataSource(
                        {
                            "xs": min_evenlope_xs,
                            "ys": self.node_levels,
                            "node_num": node_list,
                        }
                    )
                    fig.line(
                        x="xs",
                        y="ys",
                        color=color,
                        line_dash="dashed",
                        source=min_source,
                        legend_label=f"{self.cases[i]} envelope",
                        name=f"{self.cases[i]} envelope",
                        line_width=2,
                    )

                fig.legend.click_policy: str = "hide"
                fig.legend.location: str = "bottom_left"

            lay = layout([[title_div], [[self.figs]]])
            self.tabs.append(Panel(child=lay, title=f"Stage {stage}"))
        show(Tabs(tabs=self.tabs))
