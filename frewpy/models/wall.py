import os

from matplotlib.backends.backend_pdf import PdfPages  # type: ignore
import pandas as pd  # type: ignore
from typing import Dict, List

from .exceptions import FrewError
from frewpy.utils import (
    get_num_nodes,
    get_num_stages,
    get_stage_names,
    get_titles,
    get_num_design_cases,
    get_design_case_names,
)
from .plot import FrewMPL


class Wall:
    """ A class used to contain any wall related functionality of frewpy.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    get_node_levels() -> List[float]
        Get the levels of each node in the Frew model.
    get_results() -> Dict[int, dict]
        Get the shear, bending moment and displacement of the wall for each
        stage, node and design case.
    get_envelopes() -> Dict[]
    results_to_excel(out_folder: str) -> None
        Export the wall results to an excel file where each worksheet is a
        design case. The spreadsheet will be output to the folder given.

    """
    def __init__(self, json_data):
        self.json_data = json_data

    def get_node_levels(self):
        """ Method to get the levels of the nodes in a Frew model.

        Returns
        -------
        node_levels : List[float]
            The levels of each node in a Frew model.

        """
        num_nodes = get_num_nodes(self.json_data)
        try:
            node_information = self.json_data['Stages'][0]['GeoFrewNodes']
        except KeyError:
            raise FrewError('Unable to retreive node information.')
        except IndexError:
            raise FrewError('Unable to retreive node information.')

        if len(node_information) != num_nodes:
            raise FrewError('''
                Number of nodes does not equal the length of the node
                information
            ''')
        return [node_information[node]['Level'] for node in range(num_nodes)]

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
        self._check_results_present()

        wall_results: Dict[int, dict] = {}
        for stage in range(num_stages):
            wall_results[stage] = {}
            for result_set in self.json_data['Frew Results']:
                result_set_name = result_set['GeoPartialFactorSet']['Name']
                wall_results[stage][result_set_name] = {
                    'shear': [],
                    'bending': [],
                    'displacement': [],
                }
                for node in range(num_nodes):
                    stage_results = (
                        result_set['Stageresults'][stage]['Noderesults']
                    )
                    wall_results[stage][result_set_name]['shear'].append(
                        stage_results[node]['Shear']
                    )
                    wall_results[stage][result_set_name]['bending'].append(
                        stage_results[node]['Bending']
                    )
                    wall_results[stage][result_set_name][
                        'displacement'
                    ].append(
                        stage_results[node]['Displacement'] * 1000
                    )
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
        self._check_results_present()
        num_stages = get_num_stages(self.json_data)
        num_nodes = get_num_nodes(self.json_data)
        design_cases = get_design_case_names(self.json_data)
        wall_results = self.get_results()

        envelopes = {design_case: {
                'maximum': {
                    'shear': [],
                    'bending': [],
                    'disp': []
                },
                'minimum': {
                    'shear': [],
                    'bending': [],
                    'disp': []
                }
            } for design_case in design_cases}

        for design_case in design_cases:
            for node in range(num_nodes):
                shear = []
                bending = []
                disp = []

                for stage in range(num_stages):
                    shear.append(
                        wall_results[stage][design_case]['shear'][node]
                    )
                    bending.append(
                        wall_results[stage][design_case]['bending'][node]
                    )
                    disp.append(
                        wall_results[stage][design_case]['displacement'][node]
                    )

                envelopes[design_case]['maximum']['shear'].append(
                    max(shear)
                )
                envelopes[design_case]['maximum']['bending'].append(
                    max(bending)
                )
                envelopes[design_case]['maximum']['disp'].append(
                    max(disp)
                )
                envelopes[design_case]['minimum']['shear'].append(
                    min(shear)
                )
                envelopes[design_case]['minimum']['bending'].append(
                    min(bending)
                )
                envelopes[design_case]['minimum']['disp'].append(
                    min(disp)
                )
        return envelopes

    def results_to_excel(self, out_folder: str) -> None:
        """ Method to exports the wall results to an excel file where each
        sheet in the spreadsheet is a design case.

        Parameters
        ----------
        out_folder : str
            The folder path to save the results at.

        Returns
        -------
        None

        """
        if not os.path.exists(out_folder):
            raise FrewError(f'Path {out_folder} does not exist.')

        num_nodes: int = get_num_nodes(self.json_data)
        num_stages: int = get_num_stages(self.json_data)
        node_levels: List[float] = self.get_node_levels()
        wall_results: Dict[int, dict] = self.get_results()
        titles: Dict[str, str] = get_titles(self.json_data)

        job_title: str = titles['JobTitle']
        sub_title: str = titles['Subtitle'][:20]
        file_name: str = f'{job_title}_{sub_title}_results.xlsx'

        export_data: Dict[str, dict] = {}
        design_cases: List[str] = wall_results[0].keys()

        for design_case in design_cases:
            export_data[design_case] = {
                'Node #': [],
                'Node levels': [],
                'Stage': [],
                'Bending (kNm/m)': [],
                'Shear (kN/m)': [],
                'Displacement (mm)': [],
            }
            for stage in range(num_stages):
                node_array = [node for node in range(1, num_nodes+1)]
                stage_array = [stage] * num_nodes
                bending_results = wall_results[stage][design_case]['bending']
                shear_results = wall_results[stage][design_case]['shear']
                displacement_results = (
                    wall_results[stage][design_case]['displacement']
                )

                export_data[design_case]['Node #'].extend(node_array)
                export_data[design_case]['Node levels'].extend(node_levels)
                export_data[design_case]['Stage'].extend(stage_array)
                export_data[design_case]['Bending (kNm/m)'].extend(
                    bending_results
                )
                export_data[design_case]['Shear (kN/m)'].extend(shear_results)
                export_data[design_case]['Displacement (mm)'].extend(
                    displacement_results
                )
        try:
            with pd.ExcelWriter(os.path.join(out_folder, file_name)) as writer:
                for design_case in design_cases:
                    export_data_df = pd.DataFrame(export_data[design_case])
                    export_data_df.to_excel(
                        writer,
                        sheet_name=design_case,
                        index=False,
                    )
        except PermissionError:
            raise FrewError('''
                Please make sure you have closed the results spreadsheet.
            ''')

    def _check_results_present(self):
        if not self.json_data.get('Frew Results', False):
            raise FrewError('''
                No results in the model, please analyse the model first.
            ''')


# def get_wall_stiffness() -> dict:
#     """ Function to get the stiffness of the wall for each stage and node.

#     Returns
#     -------#     wall_stiffness : dict
#         The stiffness of the wall.

#     """
#     wall_stiffness = {}
#     for stage in range(0, num_stages):
#         wall_stiffness[stage] = {}
#         for node in range(0, num_nodes):
#             wall_stiffness[stage][node+1] = model.GetWallEI(
#                 node,
#                 stage
#             )
#     return wall_stiffness

    def plot_wall_results(self, out_folder: str):
        """ Method to plot the shear, bending moment and displacement of the
        wall for each stage.

        Parameters
        ----------
        out_folder : str
            The folder path to save the results at.

        Returns
        -------
        None

        """
        titles: Dict[str, str] = get_titles(self.json_data)
        num_stages: int = get_num_stages(self.json_data)
        stage_names: List[str] = get_stage_names(self.json_data)
        node_levels: List[float] = self.get_node_levels()
        wall_results: Dict[int, dict] = self.get_results()
        envelopes: Dict[str, dict] = self.get_envelopes()

        pp = PdfPages(
            f'{os.path.join(out_folder, titles["JobTitle"])}_results.pdf'
        )
        for stage in range(num_stages):
            frew_mpl = FrewMPL(
                titles,
                stage,
                stage_names[stage],
                wall_results,
                node_levels,
                envelopes
            )
            pp.savefig(frew_mpl.fig)
        pp.close()
