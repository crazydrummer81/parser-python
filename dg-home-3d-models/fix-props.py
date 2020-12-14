import os
import json
import os
from time import sleep
# from json2xml import json2xml
# from dicttoxml import dicttoxml
from datetime import datetime
import re

now = datetime.now()
current_time = now.strftime("%y%m%d-%H%M%S")
print("Current Time =", current_time)

source_folder = 'result-final/'
result_folder = 'result-fixed/'
if not os.path.isdir(result_folder):
	os.mkdir(result_folder)

files = os.listdir(source_folder)
limit = 10000
# os.remove(result_folder+target_filename)
# os.remove(result_folder+target_xml_filename)

for i, filename in enumerate(files):
	if i >= limit: break
	if not os.path.isdir(source_folder+filename):
		print('-------> '+filename+' <-------')
		with open(source_folder+filename, 'r', encoding='utf-8') as fs:
			source_dict = json.load(fs)
		props = source_dict['product_characteristics']
		fixed_props = {}
		for prop in props:
			key = [key for key in prop.keys()][0]
			value = prop[key]
			fixed_props[key] = value
		source_dict['product_characteristics'] = fixed_props
		with open(result_folder+filename, 'w', encoding='utf-8') as ft:
			json.dump(source_dict, ft, indent=2, sort_keys=False, ensure_ascii=False)

# ft.close()
# ftx.close()