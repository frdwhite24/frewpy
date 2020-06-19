import time
import os

from frewpy.models.core import (
    core_load_data,
    core_get_num_stages,
    core_get_num_nodes,
)
from frewpy.models.wall import (
    wall_get_node_levels,
    wall_get_results,
    wall_results_to_excel
)
start_time = time.time()


file_path = r"C:\Users\fred.white\Documents\windows-work\frewpy\docs_and_models\models\5b - West wall with MEFP for BM+S.json"

json_data = core_load_data(file_path)
num_stages = core_get_num_stages(json_data)
num_nodes = core_get_num_nodes(json_data, num_stages)
node_levels = wall_get_node_levels(json_data, num_nodes)
wall_results = wall_get_results(json_data, num_nodes, num_stages)
wall_results_to_excel(
    file_path,
    node_levels,
    wall_results,
    num_nodes,
    num_stages,
    )
print('finished exporting')

delta_time = time.time() - start_time
print(f'Executed in {delta_time:.2f} sec')
