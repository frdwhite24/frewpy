from frewpy import FrewModel

file_path = r"C:\Users\Fred.White\Documents\Work\Frewpy\models\SLS B4 South Basement.fwd"

model = FrewModel(file_path)

print(model.wall.get_num_nodes())


model.close()
