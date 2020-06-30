import os

from frewpy import FrewModel


# Folder which contains all the models
models_folder = r"C:\Users\fred.white\Desktop\"

# Loop through all the files in the models folder, select only json files
for file in os.listdir(models_folder):
    if file.endswith('.json'):

        # Instantiate the model with FrewModel
        model = FrewModel(os.path.join(models_folder, file))
        model.analyse()

        # Extract and plot the results all in one go
        model.wall.results_to_excel(models_folder)
        model.wall.plot_wall_results_pdf(models_folder)
