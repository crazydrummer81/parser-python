import requests #импортируем модуль
import os
import re
import time
import json

print(os.getcwd())

class Link:
	def __init__(self, img_url):
		reg = '(https?://)([0-9a-zA-Z-\._]+)([0-9a-zA-Zа-яА-Я-_\/]*?)([0-9a-zA-Zа-яА-Я-_\.]+)$'
		matches = re.match(reg, img_url)
		path = re.match('^/?(.*?)/?$', matches.group(3)) # Удаляем слеши по краям
		self.domain = matches.group(2)
		self.directory = path.group(1) # Удаляем слеши по краям
		self.filename = matches.group(4)
		self.url = img_url

urls_fileame = 'images-201217-222441.json'
result_dir = 'D:/Business/SEO/Vadim - ffleur.kz/parsing/images'
url_prefix = 'http://ffleur.ru'

# f_urls = open(urls_fileame)
with open(urls_fileame, 'r', encoding='utf-8') as fs:
	source_dict = json.load(fs)
fs.close()

i = 1
stop = 30000
pname = source_dict[0]['product_name']
inner_count = 0
for img_dict in source_dict:
	i += 1
	if img_dict['product_name'] == pname:
		inner_count += 1
	else:
		inner_count = 1
	pname = img_dict['product_name']
	if i >= stop: break
	print('----------------> ', i, ' <----------------')
	url = img_dict['url']
	print('url: %s' % url)
	link = Link(url)
	target_directory = img_dict['target_path']

	print('target_directory: %s\nlink.filename: %s' % (target_directory, link.filename))
	file_type = re.search(r'\w+$', link.filename)

	# result_filename = result_dir + '/' + target_directory + '/' + img_dict['product_id'] + '-' + img_dict['product_name'] + i
	result_filename = "%s/%s/%s-%s-%s" % (result_dir, target_directory, img_dict['product_id'], img_dict['product_name'], inner_count)
	if img_dict['variant_image']:
		result_filename = "%s/%s/%s-%s-%s" % (result_dir, target_directory, img_dict['product_id'], img_dict['variant_name'], img_dict['product_variant'])
	result_filename += '.' + file_type.group(0)


	# result_filename = result_dir + '/' + target_directory + '/' + link.filename
	# result_filename = result_dir + '/' + target_directory + '/' + link.filename
	print(result_filename)
	if os.path.exists(result_filename):
		print('%s уже скачан' % result_filename)
		continue

	img = requests.get(link.url.strip())
	print('URL: ', link.url)
	print('REQUEST: ', img)
	if (img.status_code != 200):
		print('ОШИБКА ЗАПРОСА')
	
	try:
		os.makedirs(result_dir + '/' + target_directory, mode=0o777)
	except OSError:
		print('Директория ', result_dir + '/' + target_directory, ' существует')
	else:
		print('Директория ', result_dir + '/' + target_directory, ' создана')

	img_file = open(result_filename, 'wb')
	try:
		img_file.write(img.content)
	except OSError:
		print('Файл ' + link.url + ' НЕ УДАЛОСЬ СОХРАНИТЬ')
	else:
		print('Файл ' + link.url + ' СОХРАНЕН')
	img_file.close()

	time.sleep(0.1)


