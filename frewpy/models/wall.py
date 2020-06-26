import os

import matplotlib.pyplot as plt  # type: ignore
import matplotlib.backends.backend_pdf as pltexp  # type: ignore
import pandas as pd  # type: ignore
from typing import Dict, List

from .exceptions import FrewError
from frewpy.utils import (
    get_num_nodes,
    get_num_stages,
    get_titles,
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

        if not self.json_data.get('Frew Results', False):
            raise FrewError('''
                No results in the model, please analyse the model first.
            ''')
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
                        stage_results[node]['Displacement']*1000
                    )
        return wall_results

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


# def get_envelopes() -> dict:
#     """ Function to return the envelopes of max and min shear, bending and
#     displacements.

#     """

#     wall_results = get_results()

#     envelopes = {
#         'maximum': {},
#         'minimum': {}
#     }
#     for key in envelopes:
#         envelopes[key] = {
#             # change these lists into dictionaries with node numbers so
#             # they are the same format as others
#             'shear': [],
#             'bending': [],
#             'disp': []
#         }

#     for node in range(0, num_nodes):
#         shear = []
#         bending = []
#         disp = []

#         for stage in range(0, num_stages):
#             shear.append(wall_results[stage][node+1][0])
#             bending.append(wall_results[stage][node+1][1])
#             disp.append(wall_results[stage][node+1][2])

#         envelopes['maximum']['shear'].append(max(shear))
#         envelopes['maximum']['bending'].append(max(bending))
#         envelopes['maximum']['disp'].append(max(disp))
#         envelopes['minimum']['shear'].append(min(shear))
#         envelopes['minimum']['bending'].append(min(bending))
#         envelopes['minimum']['disp'].append(min(disp))

#     return envelopes

    def plot_wall_results(self, file_path: str):
        """ Method to plot the shear, bending moment and displacement of the
        wall for each stage.

        Parameters
        ----------
        file_path : str
            The file path of the Frew model.

        Returns
        -------
        None

        """

        file_name = os.path.basename(file_path.rsplit('.', 1)[0])
        wall_results = self.get_results()
        node_levels = self.get_node_levels()
        # envelopes = self.get_envelopes()
        envelopes = []

        fp = FrewMPL(file_name, 2, wall_results, node_levels, envelopes)
