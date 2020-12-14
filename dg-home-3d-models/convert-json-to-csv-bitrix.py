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
limit = 10000

prop_keys = [
	'Бренд',
	'Вес',
	'Вид наполнения',
	'Вид подлокотников',
	'Вид спинки',
	'Вид трансформации',
	'Высота ножек',
	'Высота сиденья',
	'Высота спинки/изголовья',
	'Дизайнер (бренд) оригинала',
	'Дополнительные опции',
	'Код товара',
	'Количество мест',
	'Количество мест у товара',
	'Количество ножек',
	'Коллекция',
	'Крутящееся сиденье',
	'Куда поставить',
	'Материал',
	'Материал дверей',
	'Материал каркаса',
	'Материал обивки',
	'Материал полок',
	'Мощность 1 лампы',
	'Особенности',
	'Размер спального места',
	'Регулировка высоты сиденья',
	'Сиденье',
	'Срок гарантии',
	'Стиль',
	'Страна производства',
	'Тип (назначение, особенности)',
	'Тип спинки/изголовья',
	'Тип трансформации',
	'Тип цоколя',
	'Требуется ли сборка?',
	'Форма',
	'Цвет',
	'Цвет каркаса'
]

result_csv = ''
image_prefix = '/upload/mh'
model_prefix = '/upload/3d_models/'

for i, filename in enumerate(files):
	if i >= limit: break
	if not os.path.isdir(source_folder+filename):
		print('-------> '+filename+' <-------')
		with open(source_folder+filename, 'r', encoding='utf-8') as fs:
			source_dict = json.load(fs)

			if source_dict['product_code'] in dl_sku_list:
				model_url = model_prefix + 'mh_3d_model_art_' + 'MH-%s' % ( ('%s' % source_dict['product_code'] ).replace('DG-', '')) + '.zip'
			else:
				model_url = ''

			if len(source_dict['product_category_chain']) >= 5:
				last_cat = source_dict['product_category_chain'][len(source_dict['product_category_chain'])-1]['name']
			else:
				last_cat = ''

			target_dict = {
				"IE_XML_ID" : '"%s"' % source_dict['product_code'],
				"SKU" :  'MH-%s' % ( ('%s' % source_dict['product_code'] ).replace('DG-', '')),
				"3D_MODEL": model_url,
				# "URL": source_dict['source_url'].replace('https://dg-home.ru/', '/'),
				"NAME": source_dict['product_name'],
				"IMAGE": image_prefix + source_dict['pruduct_detail_image'],
				"PRICE_OLD": "%s" % source_dict['product_price']['old_price'],
				"PRICE_NEW": "%s" % source_dict['product_price']['new_price'],
				"IC_GROUP0": source_dict['product_category_chain'][2]['name'],
				"IC_GROUP1": source_dict['product_category_chain'][3]['name'],
				# "IC_GROUP2": source_dict['product_category_chain'][4]['name'] if len(source_dict['product_category_chain']) >=4 else '',
				"IC_GROUP2": last_cat,
				"MORE_IMAGES": ';'.join([(image_prefix + url) for url in source_dict['additional_images']]),
				"DETAIL_TEXT": re.sub(r'\s+', ' ', source_dict['product_detail_text']).strip() 
			}
			for prop in prop_keys:
				# print (prop)
				if prop in source_dict['product_characteristics']:
					target_dict[prop] = source_dict['product_characteristics'][prop]
				else:
					target_dict[prop] = ''
			target_dict['CURRENCY']
			csv_line_list = [value for value in target_dict.values()]
			# print(csv_line_list)
			csv_line = delimiter.join(csv_line_list)
			result_csv += csv_line + '\n'
			
csv_headers = '^'.join(target_dict.keys())
result_filename = 'dg-home-3d-%s.csv' % current_time
with open(result_folder+result_filename, 'w', encoding='utf-8') as ft:
	ft.write(csv_headers + '\n' + result_csv + '\n')