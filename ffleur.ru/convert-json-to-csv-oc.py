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

# Создаем список зкачанных моделей, и в CSV будет загонять только товары со скачанной моделью
dl_files_list = os.listdir('./download/')
# вытаскиваем от туда артикулы
dl_sku_list = [re.search(r'арт_(.*?)\.zip',item).group(1).strip() for item in dl_files_list]
print('ITEMS: %s' % len(dl_sku_list))

delimiter = '^'

source_folder = 'result-fixed/'
result_folder = 'csv/'
if not os.path.isdir(result_folder):
	os.mkdir(result_folder)

files = os.listdir(source_folder)
limit = 5000
csv_headers = [
	'product_id',
	'name(ru-ru)',
	'categories',
	'sku',
	'upc',
	'ean',
	'jan',
	'isbn',
	'mpn',
	'location',
	'quantity',
	'model',
	'manufacturer',
	'image_name',
	'shipping',
	'price',
	'points',
	'date_added',
	'date_modified',
	'date_available',
	'weight',
	'weight_unit',
	'length',
	'width',
	'height',
	'length_unit',
	'status',
	'tax_class_id',
	'description(ru-ru)',
	'meta_title(ru-ru)',
	'meta_description(ru-ru)',
	'meta_keywords(ru-ru)',
	'stock_status_id',
	'store_ids',
	'layout',
	'related_ids',
	'tags(ru-ru)',
	'sort_order',
	'subtract',
	'minimum'
]

categories = {
	'Лицо': 59,
	'Губы': 60,
	'Глаза': 61,
	'Брови': 62,
	'Аксессуары': 63,
	'Уход': 64,
	'Пудра и тональные средства': 65,
	'Румяна и хайлайтеры': 66,
	'Помада': 67,
	'Бальзам для губ': 68,
	'Блеск для губ': 69,
	'Карандаш для губ': 70,
	'Тушь для ресниц': 71,
	'Подводка для глаз': 72,
	'Тени для век': 73,
	'Карандаши': 74,
	'Тушь для бровей': 75,
	'Карандаш для бровей': 76,
	'Тени для бровей': 77,
	'Кисть для макияжа': 78,
	'Аппликаторы': 79,
	'Зеркало': 80,
	'Косметичка': 81,
	'Тени для век и бровей': 82
}

result_csv = ''
# image_prefix = '/upload/mh'
# model_prefix = '/upload/3d_models/'
img_base_path = 'catalog/'
product_id = 50 - 2
additional_images = []
options = []
options_db = []
options_list = []
option_id = 100 - 1
option_sort = 10
option_sort_step = 10
options_db_values = []
option_value_id = 376
options_value_sort = 10
options_value_sort_step = 10
previous_pid = ''
options_last = {}
product_options_list = []
product_attributes = []


for i, filename in enumerate(files):
	if i >= limit: break
	if not os.path.isdir(source_folder+filename):
		print('-------> '+filename+' <-------')
		with open(source_folder+filename, 'r', encoding='utf-8') as fs:
			source_dict = json.load(fs)

			product_id += 1
			try:
				weight = re.search(r'([\d,\.]+)\s*([^\s]+)', source_dict['characteristics']['Прочие']['Объём/вес нетто (1 шт.)'])
				weight_value = weight.group(1).replace('.', ',')
				weight_unit = weight.group(2)
			except:
				weight_value = ''
				weight_unit = ''

			target_dict = {
				'product_id': '%s' % source_dict['oc_product_id'],
				'name(ru-ru)': source_dict['name'],
				'categories': '%s' % categories[source_dict['category_chain'][-1]['name']],
				'sku': '',
				'upc': '',
				'ean': '',
				'jan': '',
				'isbn': '',
				'mpn': '',
				'location': '',
				'quantity': '1000',
				'model': source_dict['code'],
				'manufacturer': '',
				'image_name': 'catalog/' + source_dict['images_path'] + '/' + source_dict['detail_image_filename'],
				'shipping': 'yes',
				'price': '%s' % source_dict['price']['kzt'],
				'points': '0',
				'date_added': '',
				'date_modified': '',
				'date_available': '',
				'weight': weight_value,
				'weight_unit': weight_unit,
				'length': '0',
				'width': '0',
				'height': '0',
				'length_unit': 'см',
				'status': '',
				'tax_class_id': '',
				'description(ru-ru)': source_dict['detail_text'],
				'meta_title(ru-ru)': '',
				'meta_description(ru-ru)': '',
				'meta_keywords(ru-ru)': '',
				'stock_status_id': '7',
				'store_ids': '0',
				'layout': '0:',
				'related_ids': '',
				'tags(ru-ru)': '',
				'sort_order': '1',
				'subtract': 'false',
				'minimum': '1'
			}

			for img in source_dict['additional_images_filenames']:
				additional_images.append( str(source_dict['oc_product_id']) + delimiter + 'catalog/' + source_dict['images_path'] + '/' + img + delimiter + '0' )
			
			# print(csv_line_list)
			csv_line_list = [value for value in target_dict.values()]
			csv_line = delimiter.join(csv_line_list)
			result_csv += csv_line + '\n'

			product_variant_name = list(source_dict['characteristics']['Прочие'].keys())[-1] if\
				list(source_dict['characteristics']['Прочие'].keys())[-1] != "Наши предложения"\
				and list(source_dict['characteristics']['Прочие'].keys())[-1] != "Объём/вес нетто (1 шт.)"\
				and list(source_dict['characteristics']['Прочие'].keys())[-1] != "Артикул"\
				else ''
			try:
				product_variant_value = source_dict['characteristics']['Прочие'][product_variant_name]
			except:
				product_variant_value = ''

			option_name = product_variant_name + (' ' + source_dict['name_base']\
				if product_variant_name in ['Цвет', 'Вкус', 'Цвет карандаша', 'Тон румян из набора 2 тона', 'Палитра теней для век'] else '')
			if product_variant_name:
				oc_product_id = str(source_dict['oc_product_id'])
				base_id = oc_product_id if source_dict['id'] != previous_pid else base_id
				# if oc_product_id not in list(options.keys()):
				# 	options[oc_product_id] = options_last
				options.append({
					# 'product_id': '%s' % source_dict['oc_product_id'],
					# 'product_id': '%s' % oc_product_id,
					'product_id': oc_product_id,
					'option': option_name,
					'option_value': product_variant_value,
					'quantity': '1000',
					'subtract': 'true',
					'price': '0,00',
					'price_prefix': '+',
					'points': '0',
					'points_prefix': '+',
					'weight': '0,00',
					'weight_prefix': '+'
				})
				if [product_variant_name, source_dict['id']] not in options_list:
					options_list.append([product_variant_name, source_dict['id']])
					option_id += 1
					options_db.append({
						'option_id': str(option_id),
						'type': 'select',
						'sort_order': str(option_sort),
						'name(ru-ru)': option_name
					})
					option_sort += option_sort_step
					options_value_sort = 10
				
				try: variant_image_filename = source_dict['variant_image_filename']
				except: variant_image_filename = ''
				options_db_values.append({
					'option_value_id': f'{option_value_id}',
					'option_id': f'{option_id}',
					'image': img_base_path + source_dict['images_path'] + '/' + variant_image_filename,
					'sort_order': f'{options_value_sort}',
					'name(ru-ru)': product_variant_value
				})
				option_value_id += 1
				options_value_sort += options_value_sort_step

			if option_name: product_options_list.append({
				'product_id': f'{product_id}',
				'option': option_name,
				'default_option_value': '',
				'required': 'true'
			})

			try: product_attributes.append({
				'product_id': f'{product_id}',
				'attribute_group': 'Основные',
				'attribute': 'Объём/вес нетто (1 шт.)',
				'text(ru-ru)': source_dict['characteristics']['Прочие']['Объём/вес нетто (1 шт.)']
			})
			except: pass

			previous_pid = source_dict['id']

if not True:			
	csv_headers = delimiter.join(target_dict.keys())
	result_filename = 'ffleur.kz-%s.csv' % current_time
	with open(result_folder+result_filename, 'w', encoding='utf-8') as ft:
		ft.write(csv_headers + '\n' + result_csv + '\n')

	result_addimgs_filename = 'ffleur.kz-addimgs-%s.csv' % current_time
	with open(result_folder+result_addimgs_filename, 'w', encoding='utf-8') as ft:
		ft.write('\n'.join(additional_images))

if True:
	options_csv_list = []
	product_family = {}
	last_name = ''
	pid = options[0]['product_id']
	product_family[pid] = []
	i = -1
	for option in options:
		if last_name == option['option']:
			i += 1
			product_family[pid].append(option)
		else:
			for j in range(1, i+1):
				product_family[str(int(pid)+j)] = product_family[pid]

			i = 0
			pid = option['product_id']
			product_family[pid] = [option]
		
		last_name = option['option']
		last_id = option['product_id']
	res = []
	for fam_id in product_family.keys():
		for product in product_family[fam_id]:
			product['product_id'] = fam_id
			res.append(delimiter.join(product.values()))
	result_options_filename = 'ffleur.kz-options-values-%s.csv' % current_time
	with open(result_folder+result_options_filename, 'w', encoding='utf-8') as ft:
		ft.write('\n'.join(res))

if True:
	# product_options_dict
	result_filename = 'ffleur.kz-products-options-%s.csv' % current_time
	# result_options_db_filename = 'ffleur.kz-options-db.csv'
	p_options_list = []
	for option in product_options_list:
		p_options_list.append( delimiter.join(list(option.values())) )

	with open(result_folder+result_filename, 'w', encoding='utf-8') as ft:
		ft.write('\n'.join(p_options_list))

if True:
	# product_options_dict
	result_filename = 'ffleur.kz-products-attributes-%s.csv' % current_time
	# result_options_db_filename = 'ffleur.kz-options-db.csv'
	p_attrs_list = []
	for option in product_attributes:
		p_attrs_list.append( delimiter.join(list(option.values())) )

	with open(result_folder+result_filename, 'w', encoding='utf-8') as ft:
		ft.write('\n'.join(p_attrs_list))

# print(options_db)
if True:
	result_options_db_filename = 'ffleur.kz-options-db-%s.csv' % current_time
	# result_options_db_filename = 'ffleur.kz-options-db.csv'
	options_db_list = []
	for option_dict in options_db:
		options_db_list.append( delimiter.join(list(option_dict.values())) )

	with open(result_folder+result_options_db_filename, 'w', encoding='utf-8') as ft:
		ft.write('\n'.join(options_db_list))

# print(options_db_values)
if True:
	result_options_db_values_filename = 'ffleur.kz-options-db-values-%s.csv' % current_time
	# result_options_db_filename = 'ffleur.kz-options-db.csv'
	options_db_values_list = []
	for option_dict in options_db_values:
		options_db_values_list.append( delimiter.join(list(option_dict.values())) )

	with open(result_folder+result_options_db_values_filename, 'w', encoding='utf-8') as ft:
		ft.write('\n'.join(options_db_values_list))

# print(options_db_values)
# if True:
# 	result_products_options_filename = 'ffleur.kz-options-%s.csv' % current_time
# 	# result_options_db_filename = 'ffleur.kz-options-db.csv'
# 	options_db_values_list = []
# 	for option_dict in options_db_values:
# 		options_db_values_list.append( delimiter.join(list(option_dict.values())) )

# 	with open(result_folder+result_products_options_filename, 'w', encoding='utf-8') as ft:
# 		ft.write('\n'.join(options_db_values_list))
