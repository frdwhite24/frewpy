from pprint import pprint
import time

from frewpy import FrewModel


start_time = time.time()

file_path = r"C:\Users\Fred.White\Documents\Work\Frewpy\models\SLS B4 South Basement.fwd"
model = FrewModel(file_path)
model.analyse()
model.wall.plot_results()
model.close()

delta_time = time.time() - start_time
print(f'Executed in {delta_time:.2f} sec')
