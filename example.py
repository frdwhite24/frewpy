from frewpy import FrewModel
from pprint import pprint

file_path = r"C:\Users\Fred.White\Documents\Work\Frewpy\models\SLS B4 South Basement.fwd"
model = FrewModel(file_path)
model.analyse()
results = model.wall.get_results()

pprint(results)
pprint(results[7])


model.close()
