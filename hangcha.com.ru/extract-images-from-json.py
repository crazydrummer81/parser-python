import os
import json

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%y%m%d-%H%M%S")

IMAGE_URLS = set()

source_folder = 'result-200906-130000/'
target_folder = ''
if not os.path.isdir(target_folder) and target_folder:
	os.mkdir(target_folder)
target_filename = 'images-' + current_time + '.txt'
files = os.listdir(source_folder)

limit = 10000
with open(target_folder+target_filename, 'w+', encoding='utf-8') as ft:
	for i, filename in enumerate(files):
		if i > limit: break
		if not os.path.isdir(source_folder+filename):
			with open(source_folder+filename, 'r', encoding='utf-8') as fs:
				product = json.loads(fs.read())
				print(filename)
				IMAGE_URLS.add(product['main_image']['url'])
				# additional_images = ''
				# for image in product['additional_images']:
				# 	ft.write(image['url'] + '\n')
				for image in product['product_description']['images']:
					IMAGE_URLS.add(image['url'])
	ft.write('\n'.join(IMAGE_URLS))
