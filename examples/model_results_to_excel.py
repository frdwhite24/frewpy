import time
import os

from frewpy import core, wall
start_time = time.time()


file_path = r"C:\Users\fred.white\Documents\windows-work\frewpy\docs_and_models\models\5b - West wall with MEFP for BM+S.json"

json_data = core.load_data(file_path)
num_stages = core.get_num_stages(json_data)
num_nodes = core.get_num_nodes(json_data, num_stages)
node_levels = core.get_node_levels(json_data, num_nodes)
wall_results = wall.get_results(json_data, num_nodes, num_stages)
wall.results_to_excel(
    file_path,
    node_levels,
    wall_results,
    num_nodes,
    num_stages,
    )
print('finished exporting')

delta_time = time.time() - start_time
print(f'Executed in {delta_time:.2f} sec')
