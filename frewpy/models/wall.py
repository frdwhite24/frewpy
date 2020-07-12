"""
Wall
====

This module holds the class for the Wall object.

"""

import os
from typing import Dict, List, Union
from uuid import uuid4
from datetime import datetime
import re

from matplotlib.backends.backend_pdf import PdfPages  # type: ignore
import pandas as pd  # type: ignore

from frewpy.utils import (
    get_num_nodes,
    get_num_stages,
    get_stage_names,
    get_titles,
    get_design_case_names,
    check_results_present,
)
from .plot import FrewMPL, FrewBokeh
from .exceptions import FrewError


class Wall:
    """ A class used to contain any wall related functionality of frewpy.

    """

    def __init__(self, json_data):
        self.json_data = json_data

    def get_node_levels(self) -> List[float]:
        """ Method to get the levels of the nodes in a Frew model.

        Returns
        -------
        node_levels : List[float]
            The levels of each node in a Frew model.

        """
        num_nodes = get_num_nodes(self.json_data)
        try:
            node_information = self.json_data["Stages"][0]["GeoFrewNodes"]
        except KeyError:
            raise FrewError("Unable to retreive node information.")
        except IndexError:
            raise FrewError("Unable to retreive node information.")

        if len(node_information) != num_nodes:
            raise FrewError(
                """
                Number of nodes does not equal the length of the node
                information
            """
            )
        return [node_information[node]["Level"] for node in range(num_nodes)]

    def get_results(self) -> Dict[int, dict]:
        """ Method to get the shear, bending moment and displacement of the
        wall for each stage, node, and design case.

        Returns
        -------
        wall_results : Dict[int, dict]
            The shear, bending and displacement of the wall.

        """
        num_nodes = get_num_nodes(self.json_data)
        num_stages = get_num_stages(self.json_data)
        check_results_present(self.json_data)

        wall_results: Dict[int, dict] = {}
        for stage in range(num_stages):
            wall_results[stage] = {}
            for result_set in self.json_data["Frew Results"]:
                result_set_name = result_set["GeoPartialFactorSet"]["Name"]
                wall_results[stage][result_set_name] = {
                    "shear": [],
                    "bending": [],
                    "displacement": [],
                }
                for node in range(num_nodes):
                    stage_results = result_set["Stageresults"][stage][
                        "Noderesults"
                    ]
                    wall_results[stage][result_set_name]["shear"].append(
                        stage_results[node]["Shear"] / 1000
                    )
                    wall_results[stage][result_set_name]["bending"].append(
                        stage_results[node]["Bending"] / 1000
                    )
                    wall_results[stage][result_set_name][
                        "displacement"
                    ].append(stage_results[node]["Displacement"] * 1000)
        return wall_results

    def get_envelopes(self) -> Dict[str, dict]:
        """ Method to return the envelopes of max and min shear, bending and
        displacements for each design case.

        Returns
        -------
        envelopes : Dict[str, dict]
            The maximum and minimum shear, bending and displacement for each
            design case for all stages.

        """
        check_results_present(self.json_data)
        num_stages = get_num_stages(self.json_data)
        num_nodes = get_num_nodes(self.json_data)
        design_cases = get_design_case_names(self.json_data)
        wall_results = self.get_results()

        envelopes: Dict[str, dict] = {
            design_case: {
                "maximum": {"shear": [], "bending": [], "disp": []},
                "minimum": {"shear": [], "bending": [], "disp": []},
            }
            for design_case in design_cases
        }

        for design_case in design_cases:
            for node in range(num_nodes):
                shear = []
                bending = []
                disp = []

                for stage in range(num_stages):
                    shear.append(
                        wall_results[stage][design_case]["shear"][node]
                    )
                    bending.append(
                        wall_results[stage][design_case]["bending"][node]
                    )
                    disp.append(
                        wall_results[stage][design_case]["displacement"][node]
                    )

                envelopes[design_case]["maximum"]["shear"].append(max(shear))
                envelopes[design_case]["maximum"]["bending"].append(
                    max(bending)
                )
                envelopes[design_case]["maximum"]["disp"].append(max(disp))
                envelopes[design_case]["minimum"]["shear"].append(min(shear))
                envelopes[design_case]["minimum"]["bending"].append(
                    min(bending)
                )
                envelopes[design_case]["minimum"]["disp"].append(min(disp))
        return envelopes

    def results_to_excel(self, out_folder: str) -> None:
        """ Method to exports the wall results to an excel file where each
        sheet in the spreadsheet is a design case. The spreadsheet also
        a title sheet and the envelopes.

        Parameters
        ----------
        out_folder : str
            The folder path to save the results at.

        Returns
        -------
        None

        """
        if not os.path.exists(out_folder):
            raise FrewError(f"Path {out_folder} does not exist.")

        num_nodes: int = get_num_nodes(self.json_data)
        num_stages: int = get_num_stages(self.json_data)
        node_levels: List[float] = self.get_node_levels()
        wall_results: Dict[int, dict] = self.get_results()
        design_cases: List[str] = get_design_case_names(self.json_data)
        envelopes: Dict[str, dict] = self.get_envelopes()
        export_envelopes = pd.DataFrame(
            self._format_envelope_data(
                num_nodes, node_levels, envelopes, design_cases
            )
        )
        titles: Dict[str, str] = get_titles(self.json_data)
        export_titles = pd.DataFrame(self._format_titles_data(titles))

        job_title: str = titles["JobTitle"]
        uuid_str: str = str(uuid4()).split("-")[0]
        file_name: str = f"{job_title}_{uuid_str}_results.xlsx"

        export_data: Dict[str, dict] = {}
        for design_case in design_cases:
            export_data[design_case] = {
                "Node #": [],
                "Node levels (m)": [],
                "Stage": [],
                "Bending (kNm/m)": [],
                "Shear (kN/m)": [],
                "Displacement (mm)": [],
            }
            for stage in range(num_stages):
                node_array = list(range(1, num_nodes + 1))
                stage_array = [stage] * num_nodes
                bending_results = wall_results[stage][design_case]["bending"]
                shear_results = wall_results[stage][design_case]["shear"]
                displacement_results = wall_results[stage][design_case][
                    "displacement"
                ]

                export_data[design_case]["Node #"].extend(node_array)
                export_data[design_case]["Node levels (m)"].extend(node_levels)
                export_data[design_case]["Stage"].extend(stage_array)
                export_data[design_case]["Bending (kNm/m)"].extend(
                    bending_results
                )
                export_data[design_case]["Shear (kN/m)"].extend(shear_results)
                export_data[design_case]["Displacement (mm)"].extend(
                    displacement_results
                )
        try:
            with pd.ExcelWriter(os.path.join(out_folder, file_name)) as writer:
                export_titles.to_excel(
                    writer, sheet_name="Titles", index=False, header=False
                )
                export_envelopes.to_excel(
                    writer, sheet_name="Envelopes", index=False,
                )
                for design_case in design_cases:
                    export_data_df = pd.DataFrame(export_data[design_case])
                    export_data_df.to_excel(
                        writer, sheet_name=design_case, index=False,
                    )
        except PermissionError:
            raise FrewError(
                """
                Please make sure you have closed the results spreadsheet.
            """
            )

    def _format_titles_data(
        self, titles: Dict[str, str]
    ) -> Dict[str, List[str]]:
        format_titles: Dict[str, List[str]] = {
            "title": [],
            "value": [],
        }
        [format_titles["title"].append(item) for item in titles.keys()]
        [format_titles["value"].append(item) for item in titles.values()]
        format_titles["title"].append("DateExported")
        format_titles["value"].append(datetime.now().strftime(r"%d/%m/%Y"))

        for index, title in enumerate(format_titles["title"]):
            # Regex: finds all upper case letters within the string, not at the
            # start of the string and then prefixes them with a space.
            matches = re.findall(r"\B[A-Z]", title)
            if matches:
                for match in matches:
                    title = title.replace(match, f" {match}").strip()
                format_titles["title"][index] = title
        return format_titles

    def _format_envelope_data(
        self,
        num_nodes: int,
        node_levels: List[float],
        envelopes: Dict[str, dict],
        design_cases: List[str],
    ) -> Dict[str, list]:
        format_envelopes: Dict[str, list] = {
            "Design case": [],
            "Node #": [],
            "Node levels (m)": [],
            "Max Bending (kNm/m)": [],
            "Min Bending (kNm/m)": [],
            "Max Shear (kN/m)": [],
            "Min Shear (kN/m)": [],
            "Max Displacement (mm)": [],
            "Min Displacement (mm)": [],
        }
        [
            format_envelopes["Design case"].extend([design_case] * num_nodes)
            for design_case in design_cases
        ]
        for design_case in design_cases:
            format_envelopes["Node #"].extend(list(range(1, num_nodes + 1)))
            format_envelopes["Node levels (m)"].extend(node_levels)
            format_envelopes["Max Bending (kNm/m)"].extend(
                envelopes[design_case]["maximum"]["bending"]
            )
            format_envelopes["Min Bending (kNm/m)"].extend(
                envelopes[design_case]["minimum"]["bending"]
            )
            format_envelopes["Max Shear (kN/m)"].extend(
                envelopes[design_case]["maximum"]["shear"]
            )
            format_envelopes["Min Shear (kN/m)"].extend(
                envelopes[design_case]["minimum"]["shear"]
            )
            format_envelopes["Max Displacement (mm)"].extend(
                envelopes[design_case]["maximum"]["disp"]
            )
            format_envelopes["Min Displacement (mm)"].extend(
                envelopes[design_case]["minimum"]["disp"]
            )
        return format_envelopes

    def _get_plot_data(self) -> Dict[str, Union[dict, int, list]]:
        return {
            "titles": get_titles(self.json_data),
            "num_stages": get_num_stages(self.json_data),
            "stage_names": get_stage_names(self.json_data),
            "node_levels": self.get_node_levels(),
            "wall_results": self.get_results(),
            "envelopes": self.get_envelopes(),
        }

    def plot_results_pdf(self, out_folder: str) -> None:
        """ Method to plot the shear, bending moment and displacement of the
        wall for each stage. Output is a static pdf plot created using the
        Matplotlib plotting library.

        Parameters
        ----------
        out_folder : str
            The folder path to save the results at.

        Returns
        -------
        None

        """
        plot_data_dict = self._get_plot_data()
        job_title: str = plot_data_dict["titles"]["JobTitle"]
        uuid_str: str = str(uuid4()).split("-")[0]
        out_pdf_name: str = f"{job_title}_{uuid_str}_results.pdf"

        try:
            out_file = PdfPages(os.path.join(out_folder, out_pdf_name))
        except PermissionError:
            raise FrewError(
                f"Please make sure {out_pdf_name} is closed first."
            )

        for stage in range(plot_data_dict["num_stages"]):
            frew_mpl = FrewMPL(
                plot_data_dict["titles"],
                stage,
                plot_data_dict["stage_names"][stage],
                plot_data_dict["wall_results"],
                plot_data_dict["node_levels"],
                plot_data_dict["envelopes"],
            )
            out_file.savefig(frew_mpl.fig)
        out_file.close()

    def plot_results_html(self, out_folder: str):
        """ Method to plot the shear, bending moment and displacement of the
        wall for each stage. Output is a interactive html plot created using
        the Bokeh plotting library.

        Parameters
        ----------
        out_folder : str
            The folder path to save the results at.

        Returns
        -------
        None

        """
        plot_data_dict: Dict[str, Union[dict, int, list]] = (
            self._get_plot_data()
        )

        job_title: str = plot_data_dict["titles"]["JobTitle"]
        uuid_str: str = str(uuid4()).split("-")[0]
        out_html_name: str = f"{job_title}_{uuid_str}_results.html"

        output_file: str = os.path.join(out_folder, out_html_name)

        frew_bp = FrewBokeh(
            output_file,
            plot_data_dict["titles"],
            plot_data_dict["num_stages"],
            plot_data_dict["stage_names"],
            plot_data_dict["wall_results"],
            plot_data_dict["node_levels"],
            plot_data_dict["envelopes"],
        )
        frew_bp.plot()

    def get_wall_stiffness(self) -> Dict[int, List[float]]:
        """ Function to get the stiffness of the wall for each stage and node.

        Returns
        -------
        wall_stiffness : Dict[int, List[float]]
            The stiffness of the wall in kNm2/m for each stage.

        """
        num_stages = get_num_stages(self.json_data)
        wall_stiffness: Dict[int, List[float]] = {}

        for stage in range(num_stages):
            wall_stiffness[stage] = [
                item["Eival"] / 1000
                for item in self.json_data["Stages"][stage]["GeoFrewNodes"]
            ]
        return wall_stiffness
