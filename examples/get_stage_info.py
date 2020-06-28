import os

from frewpy import FrewModel


# File path to the model
file_path = r"C:\Users\fred.white\Desktop\example_model.json"

# Instantiate the model with FrewModel and then get the stage information
model = FrewModel(file_path)
num_stages = model.get('num stages')
stage_names = model.get('stage names')

# Loop through the stages and print the name and number of the stage
for stage in range(num_stages):
    print(f'Stage {stage}: {stage_names[stage]}')
