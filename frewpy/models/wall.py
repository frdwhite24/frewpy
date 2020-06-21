import matplotlib.pyplot as plt  # type: ignore
import matplotlib.backends.backend_pdf as pltexp  # type: ignore
import pandas as pd  # type: ignore
from typing import Dict, List

from .exceptions import FrewError


def get_node_levels(json_data: dict, num_nodes: int) -> list:
    """ Function to get the levels of the nodes in a Frew model.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.
    num_nodes : int
        The number of nodes in the Frew model.

    Returns
    -------
    node_levels : list
        The levels of each node in a Frew model.

    """
    try:
        node_information = json_data['Stages'][0]['GeoFrewNodes']
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


def get_results(json_data: dict, num_nodes: int, num_stages: int) -> dict:
    """ Function to get the shear, bending moment and displacement of the
    wall for each stage and node.

    Parameters
    ----------
    json_data : dict
        A Python dictionary of the data held within the json model file.
    num_nodes : int
        The number of nodes in the Frew model.
    num_stages : int
        The number of stages in the Frew model.

    Returns
    -------
    wall_results : dict
        The shear, bending and displacement of the wall.

    """
    if not json_data.get('Frew Results', False):
        raise FrewError('''
            No results in the model, please analyse the model first.
        ''')
    wall_results: Dict[int, dict] = {}
    for stage in range(num_stages):
        wall_results[stage] = {}
        for result_set in json_data['Frew Results']:
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
                wall_results[stage][result_set_name]['displacement'].append(
                    stage_results[node]['Displacement']*1000
                )
    return wall_results


def results_to_excel(
    file_path: str,
    node_levels: list,
    wall_results: dict,
    num_nodes: int,
    num_stages: int,
) -> None:
    """ Exports the wall results to an excel file where each sheet in the
    spreadsheet is a design case.

    Parameters
    ----------
    file_path : str
        The file path of the model. This will be used to export the spreadsheet
        to, and to name the spreadsheet.
    node_levels : list
        The levels of each node in a Frew model.
    wall_results : dict
        The shear, bending and displacement of the wall.
    num_nodes : int
        The number of nodes in the Frew model.
    num_stages : int
        The number of stages in the Frew model.

    Returns
    -------
    None

    """
    export_data: Dict[str, dict] = {}
    design_cases: List[str] = wall_results[0].keys()
    excel_path = f'{file_path.rsplit(".", 1)[0]}_results.xlsx'

    for design_case in design_cases:
        export_data[design_case] = {
            'Node levels': [],
            'Stage': [],
            'Bending': [],
            'Shear': [],
            'Displacement': [],
        }
        for stage in range(num_stages):
            stage_array = [stage] * num_nodes
            bending_results = wall_results[stage][design_case]['bending']
            shear_results = wall_results[stage][design_case]['shear']
            displacement_results = (
                wall_results[stage][design_case]['displacement']
            )

            export_data[design_case]['Node levels'].extend(node_levels)
            export_data[design_case]['Stage'].extend(stage_array)
            export_data[design_case]['Bending'].extend(bending_results)
            export_data[design_case]['Shear'].extend(shear_results)
            export_data[design_case]['Displacement'].extend(
                displacement_results
            )

    with pd.ExcelWriter(excel_path) as writer:
        for design_case in design_cases:
            export_data_df = pd.DataFrame(export_data[design_case])
            export_data_df.to_excel(writer, sheet_name=design_case)

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


# def plot_results() -> None:
#     """ Function to plot the shear, bending moment and displacement of the
#     wall for each stage.

#     """

#     file_name = os.path.basename(file_path.rsplit('.', 1)[0])
#     wall_results = get_results()
#     node_levels = get_node_levels()
#     envelopes = get_envelopes()

#     # Set defaults for plot styling
#     plt.rcParams.update({'axes.titlesize': 10})
#     plt.rcParams.update({'axes.labelsize': 7})
#     plt.rcParams.update({'xtick.labelsize': 7})
#     plt.rcParams.update({'ytick.labelsize': 7})

#     pdf = pltexp.PdfPages(
#         f'{os.path.join(folder_path, file_name)}_results.pdf'
#     )
#     for stage in range(0, num_stages):
#         figure_title = f'{file_name} - Stage {stage}'

#         plt.close('all')
#         fig, (ax1, ax2, ax3) = plt.subplots(
#             1,
#             3,
#             sharey=True)

#         # Figure information
#         fig.suptitle(figure_title)

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
