import os
import json
import os
from time import sleep
# from json2xml import json2xml
# from dicttoxml import dicttoxml
from datetime import datetime
import re
from translit import transliterate

def csv_join(csv_list, delimiter = '^'):
	res = ''
	for item in csv_list:
		res += delimiter.join(item)
		res += '\n'
	return res

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
limit = 2500

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

part_n = 2000
part_i = 0
part = []
parts = []

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

			# if len(source_dict['product_category_chain']) >= 6:
			# 	last_cat = source_dict['product_category_chain'][len(source_dict['product_category_chain'])-1]['name']
			# else:
			# 	last_cat = ''

			target_dict = {
				"IE_XML_ID" : '"%s"' % source_dict['product_code'],
				"SKU" :  'MH-%s' % ( ('%s' % source_dict['product_code'] ).replace('DG-', '')),
				"3D_MODEL": model_url.replace('MH-', ''),
				# "URL": source_dict['source_url'].replace('https://dg-home.ru/', '/'),
				"NAME": source_dict['product_name'],
				"NAME_ALIAS": transliterate(source_dict['product_name']).lower(),
				"IMAGE": image_prefix + source_dict['pruduct_detail_image'],
				"PRICE_OLD": "%s" % source_dict['product_price']['old_price'],
				"PRICE_NEW": "%s" % source_dict['product_price']['new_price'],
				# "IC_GROUUP3": last_cat,
				# "MORE_IMAGES": ';'.join([(image_prefix + url) for url in source_dict['additional_images']]),
				"DETAIL_TEXT": re.sub(r'\s+', ' ', source_dict['product_detail_text']).strip() 
			}
			target_dict["IC_GROUP5_ALIAS"] = 'Y' if target_dict['3D_MODEL'] else 'N'

			for ic in range(6):
				# print(i,cat)
				if ic < len(source_dict['product_category_chain']):
					value = source_dict['product_category_chain'][ic]['name'] \
						.replace('Барныестулья', 'Барные')\
						.replace('Барные стулья', 'Барные')\
						.replace('Настенный декор', 'Настенный')\
						.replace('Объмный декор', 'Объемный')\
						.replace('Журнальные и кофейные столы', 'Журнальные')\
						.replace('Обеденные столы', 'Обеденные')\
						.replace('Рабочие  столы', 'Письменные')\
						.replace('Полки вешалки крючки', 'Вешалки')
					target_dict["IC_GROUP%s" % ic] = value
					target_dict["IC_GROUP%s_ALIAS" % ic] = transliterate(value).lower()
					# target_dict["IC_GROUP_3D%s" % i] = value
				else:
					target_dict["IC_GROUP%s" % ic] = ''
					target_dict["IC_GROUP%s_ALIAS" % ic] = ''
					# target_dict["IC_GROUP_3D%s" % ic] = ''
				
				target_dict["IC_GROUP0_ALIAS"] = 'html'
				target_dict["IC_GROUP1"] = '3D-модели'
				target_dict["IC_GROUP1_ALIAS"] = image_prefix + source_dict['pruduct_detail_image']
				

				if int(source_dict["product_price"]["old_price"]) == 0:
					target_dict["PRICE_OLD"] = str(source_dict["product_price"]["new_price"])


			for prop in prop_keys:
				# print (prop)
				if prop in source_dict['product_characteristics']:
					target_dict[prop] = source_dict['product_characteristics'][prop]
					if prop in ['Вес', 'Высота сиденья', 'Высота ножек']:
						target_dict[prop] = target_dict[prop].replace(' ', '').replace('.', ',').replace('DG-HOME', '')
				else:
					target_dict[prop] = ''
			target_dict['CURRENCY'] = 'RUB'
			target_dict['Бренд'] = target_dict['Бренд'].replace('DG-HOME', '')

			
			# print(csv_line_list)
			if len(source_dict['additional_images'])  == 0:
				csv_line_list = [value for value in target_dict.values()]
				part.append(csv_line_list)

			for img in source_dict['additional_images']:
				target_dict['MORE_IMAGES'] = image_prefix + img
				csv_line_list = [value for value in target_dict.values()]
				part.append(csv_line_list)
				csv_line = delimiter.join(csv_line_list)
				result_csv += csv_line + '\n'

			if i%part_n == 0 and i > 0:
				# print('part_i:', part_i)
				parts.append(part)
				part = []
				part_i += 1
parts.append(part) # Добавляем последнюю часть

			
csv_headers = '^'.join(target_dict.keys())

if True:
	result_filename = 'dg-home-3d-all-%s.csv' % current_time
	with open(result_folder+result_filename, 'w', encoding='utf-8') as ft:
		ft.write(csv_headers + '\n' + result_csv + '\n')

if True:
	print('=============== WRITE PARTS TO FILES ==================')
	# print(parts); exit()
	for i, part in enumerate(parts):
		print(f'---------------- PART {i} ---------------------')
		result_filename =  f'dg-home-3d-{i:05d}.csv'
		with open(result_folder+result_filename, 'w', encoding='utf-8') as ft:
			ft.write(csv_headers + '\n' + csv_join(part))
