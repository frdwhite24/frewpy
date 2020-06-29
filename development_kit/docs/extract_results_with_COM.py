import win32com.client
import os
from pprint import pprint

model = win32com.client.Dispatch("frewLib.FrewComAuto")

CURR_DIR = os.getcwd()

models = []

for file in os.listdir(CURR_DIR):
    if file.endswith('.fwd') or file.endswith('.FWD'):
        models.append(file)

for model_name in models:
    model.Open(os.path.join(CURR_DIR, model_name))
    model.DeleteResults()
    num_stages = model.GetNumStages()
    num_nodes = model.GetNumNodes()
    model.Analyse(num_stages-1)

    wall_results = {}
    for stage in range(0, num_stages):
        wall_results[stage] = {}
        for node in range(0, num_nodes):
            wall_results[stage][node+1] = [
                model.GetNodeShear(node, stage),
                model.GetNodeBending(node, stage),
                model.GetNodeDisp(node, stage)
            ]

    model.Close()

    pprint(wall_results)
