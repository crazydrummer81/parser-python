import os
import json
import re

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%y%m%d-%H%M%S")

propertiesGroups = set()
properties = set()
propertiesWithValues = set()

source_folder = 'result-fixed/'
target_folder = 'result-options/'
img_base_path = '/image/catalog'
if not os.path.isdir(target_folder):
	os.mkdir(target_folder)
target_filename_0 = current_time + '-groups-' + '.csv'
target_filename_1 = current_time + '-groups-properties-' + '.csv'
target_filename_2 = current_time + '-groups-properties-values-' + '.csv'
files = os.listdir(source_folder)

divider = '\t'
option_id = 100
limit = 5000
# ft0 = open(target_folder+target_filename_0, 'w', encoding='utf-8')
ft1 = open(target_folder+target_filename_1, 'w', encoding='utf-8')
ft2 = open(target_folder+target_filename_2, 'w', encoding='utf-8')
for i, filename in enumerate(files):
	if i > limit: break
	if not os.path.isdir(source_folder+filename):
		with open(source_folder+filename, 'r', encoding='utf-8') as fs:
			product = json.loads(fs.read())
			print(filename)
			
			# Формирование результата по продукту
			prodProps = product['characteristics']
			for group in prodProps:
				propertiesGroups.add(group)
				print('group: %s' % group)
				
				for prop in prodProps[group]:
					print('prop: %s' % prop)
					key = prop
					value = prodProps[group][key]
					if prop not in ['Артикул', 'Наши предложения', 'Объём/вес нетто (1 шт.)']:
						try:
							img = img_base_path + '/'+ product['images_path'] + '/' + product['variant_image_filename']
						except:
							img = ''
					else: img = ''
					if key == 'Цвет':
						key += ' ' + re.sub(r',[^,]*$', '', product['name']) 
					properties.add(divider.join([group, key]))
					propertiesWithValues.add(divider.join([key, img, value]))

			csv_line = [
				'option_id': str(option_id),
				'type': 'select',
				'sort_order': str(i+1 * 10),
				'name(ru-ru)': ''
			]

			option_id += 1
			

# Запись результата в файл
# ft0.write('\n'.join(sorted(propertiesGroups)))
ft1.write('\n'.join(sorted(properties)))
ft2.write('\n'.join(sorted(propertiesWithValues)))
# ft0.close()
ft1.close()
ft2.close()
