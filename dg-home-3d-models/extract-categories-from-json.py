import os
import json

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%y%m%d-%H%M%S")
CATEGORIES = set()

source_folder = 'result-200907-092549/'
target_folder = './'
if not os.path.isdir(target_folder):
	os.mkdir(target_folder)
target_filename = 'categories-' + current_time + '.txt'
files = os.listdir(source_folder)

limit = 10000
with open(target_folder+target_filename, 'w+', encoding='utf-8') as ft:
	for i, filename in enumerate(files):
		if i > limit: break
		if not os.path.isdir(source_folder+filename):
			with open(source_folder+filename, 'r', encoding='utf-8') as fs:
				product = json.loads(fs.read())
				print(filename)
				# for categorie in product['product_category_chain']:
				CATEGORIES.add('^'.join([categorie for categorie in product['product_category_chain']]))
	ft.write('\n'.join(CATEGORIES))
