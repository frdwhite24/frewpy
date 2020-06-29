import os

from frewpy import FrewModel


# Model file path and the folder in which to save the results
file_path = r"C:\Users\fred.white\Desktop\example_model.json"
folder_path = os.path.dirname(file_path)

# Instantiate the model with FrewModel and then plot the results
model = FrewModel(file_path)
model.analyse()
model.wall.plot_wall_results_pdf(folder_path)
