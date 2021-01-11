import os
import json
from translit import translit

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%y%m%d-%H%M%S")

IMAGES = []

source_folder = 'result-fixed/'
target_folder = ''
if not os.path.isdir(target_folder) and target_folder:
	os.mkdir(target_folder)
target_filename = 'images-' + current_time + '.json'
files = os.listdir(source_folder)

images = []
limit = 10000
with open(target_folder+target_filename, 'w+', encoding='utf-8') as ft:
	for i, filename in enumerate(files):
		if i > limit: break
		if not os.path.isdir(source_folder+filename):
			with open(source_folder+filename, 'r', encoding='utf-8') as fs:
				product = json.loads(fs.read())
				print(filename)

				idx = list(product['characteristics']['Прочие'].keys())[-1] if list(product['characteristics']['Прочие'].keys())[-1] != "Артикул" else ''
				product_variant = translit(product['characteristics']['Прочие'][idx]) if idx != '' else ''
				product_variant = product_variant

				IMAGES.append({ \
					'name': product['name'], \
					'url': product['detail_image'], \
					'target_path': product['images_path'], \
					'product_id': product['id'], \
					'product_name': translit(product['name']), \
					'product_variant': product_variant, \
					'variant_image': False })

				for image in product['additional_images']:
					IMAGES.append({ \
						'name': product['name'], \
						'url': image, \
						'target_path': product['images_path'], \
						'product_id': product['id'],\
						'product_name': translit(product['name']), \
						'product_variant': product_variant, \
						'variant_image': False }) 

				if product['variant_image']:
					IMAGES.append({ \
						'name': product['name'], \
						'url': product['variant_image'], \
						'target_path': product['images_path'], \
						'product_id': product['id'],
						'product_name': translit(product['name']), \
						'product_variant': product_variant, \
						'variant_image': True,
						'variant_name': translit(list(product['characteristics']['Прочие'].keys())[-1]) }) 
				

	# ft.write('\n'.join(IMAGES))
	ft.write(json.dumps(IMAGES, indent=2, sort_keys=False, ensure_ascii=False))
