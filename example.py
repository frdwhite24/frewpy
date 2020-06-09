from pprint import pprint
import time

from frewpy.frewpy import FrewModel


start_time = time.time()

file_path = r"C:\Users\Fred.White\Documents\Work\Frewpy\models\2020-03-05 1200mm pile toe @ -20mOD Base Model -  SLS.fwd"
model = FrewModel(file_path)
model.analyse()

wall_results = model.wall.get_results()
net_deflections = {}
for stage in range(0, model.num_stages):
    if not stage == 0 and not stage == 5:
        net_deflections[stage] = {}
        for node in range(0, model.num_nodes):
            net_deflections[stage][node+1] = (
                wall_results[stage][node+1][2]
                - wall_results[stage-1][node+1][2]
            )
    if stage == 6:
        net_deflections[stage] = {}
        for node in range(0, model.num_nodes):
            net_deflections[stage][node+1] = (
                wall_results[stage][node+1][2]
                - wall_results[stage-2][node+1][2]
            )

net_total_pressures = model.calculate.net_total_pressures()

node_levels = model.wall.get_node_levels()
node_thickness = {}
for node in range(0, model.num_nodes):
    if not node == model.num_nodes-1:
        node_thickness[node+1] = (
            node_levels[node+1]
            - node_levels[node+2]
        )
    else:
        node_thickness[node+1] = 0

force_per_m = {}
for stage in range(0, model.num_stages):
    force_per_m[stage] = {}
    for node in range(0, model.num_nodes):
        force_per_m[stage][node+1] = (
            net_total_pressures[stage][node+1]
            * node_thickness[node+1]
        )


pprint(net_total_pressures[4])
pprint(node_thickness)
pprint(force_per_m[4])


model.close()

delta_time = time.time() - start_time
print(f'Executed in {delta_time:.2f} sec')
