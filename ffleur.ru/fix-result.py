import os
import json
import os
from time import sleep
# from json2xml import json2xml
# from dicttoxml import dicttoxml
from datetime import datetime
import re
import price
from translit import translit

def fextention(filename):
	# Извлечение расширения из имени файла
	return re.search(r'\.\w+$', filename).group(0)

now = datetime.now()
current_time = now.strftime("%y%m%d-%H%M%S")
print("Current Time =", current_time)

source_folder = 'result-201216-200000/'
result_folder = 'result-fixed/'

# Формируем словарь из json-файла картинок
imges_json = 'images-210104-140913.json'
with open(imges_json, 'r', encoding='utf-8') as fs:
	images_dict = json.load(fs)
fs.close()

if not os.path.isdir(result_folder):
	os.mkdir(result_folder)

files = os.listdir(source_folder)
limit = 2000
# os.remove(result_folder+target_filename)
# os.remove(result_folder+target_xml_filename)
oc_product_id = 49

for i, filename in enumerate(files):
	if i >= limit: break
	if not os.path.isdir(source_folder+filename):
		print('-------> '+filename+' <-------')
		with open(source_folder+filename, 'r', encoding='utf-8') as fs:
			target_dict = json.load(fs)

		# Добавляем бвзовое название (без опции)
		base_name = ' ' + re.sub(r',[^,]*$', '', target_dict['name'])
		target_dict['name_base'] = base_name.strip()

		# Добавляем уникальный код для для опций вида: Артикул + Цвет
		last_key = list(target_dict['characteristics']['Прочие'].keys())[-1]
		code = target_dict['characteristics']['Прочие']['Артикул'] + (' - ' + target_dict['characteristics']['Прочие'][last_key] if last_key != 'Артикул' else '')
		target_dict['code'] = code
		target_dict['oc_product_id'] = oc_product_id
		oc_product_id += 1

		# Добавляем цены в тенге
		target_dict['price']['kzt'] = price.price_dict[target_dict['id']]

		# Приводим категории к нижнему регистру
		for i, cat in enumerate(target_dict['category_chain']):
			target_dict['category_chain'][i]['name'] = target_dict['category_chain'][i]['name'][0] + target_dict['category_chain'][i]['name'][1:].lower()

		# Добавляем путь к картинкам по категории и ID товара
		directory = '/'.join([translit(cat['name'].lower()) for cat in target_dict['category_chain'][2:]])
		images_path = '%s/%s' % ( directory , target_dict['id'] )
		target_dict['images_path'] = images_path

		# Вытаскиваем из словаря картинок все с нужным id
		product_id = target_dict['id']
		imgs = []
		# for img in images_dict:
			# if img.product_id == product_id:
			# 	imgs.append(img)

		# Определяем имя основной картинки
		i = 0
		target_dict['additional_images_filenames'] = []
		for img in images_dict:
			if target_dict['detail_image'] == img['url']:
				i += 1
				target_dict['detail_image_filename'] = target_dict['id'] + '-' + img['product_name'] + ('-%s' % i) + fextention(target_dict['detail_image'])

		for img in images_dict:
			if img['name'] == target_dict['name']:

				# for timg in target_dict['additional_images']:
					# Определяем имя доп. картинок
				if img['variant_image']:
					target_dict['variant_image_filename'] = '%s-%s-%s%s' % ( img['product_id'], img['variant_name'], img['product_variant'], fextention(img['url']) )
				elif img['url'] in target_dict['additional_images']:
					i += 1
					target_dict['additional_images_filenames'].append( '%s-%s-%s%s' % (target_dict['id'], img['product_name'], i, fextention(img['url'])) )
				else:
					# print(img['url'] + '-'*20)
					pass


		with open(result_folder+filename, 'w', encoding='utf-8') as ft:
			json.dump(target_dict, ft, indent=2, sort_keys=False, ensure_ascii=False)

# ft.close()
# ftx.close()
