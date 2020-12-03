import requests #импортируем модуль
import os
import re
import time

print(os.getcwd())

class Link:
	def __init__(self, img_url):
		reg = '(https?://)([0-9a-zA-Z-\._]+)([0-9a-zA-Zа-яА-Я-_\./]*?)([0-9a-zA-Zа-яА-Я-_\.]+)$'
		matches = re.match(reg, img_url)
		path = re.match('^/?(.*?)/?$', matches.group(3)) # Удаляем слеши по краям
		self.domain = matches.group(2)
		self.directory = path.group(1) # Удаляем слеши по краям
		self.filename = matches.group(4)
		self.url = img_url

urls_fileame = 'images-200906-161849.txt'
result_dir = 'images'
url_prefix = ''

f_urls = open(urls_fileame)

i = 0
for line in f_urls:
	i += 1
	print('----------------> ', i, ' <----------------')
	link = Link(url_prefix + line)
	img = requests.get(link.url.strip())
	print('URL: ', link.url)
	print('REQUEST: ', img)
	if (img.status_code != 200):
		print('ОШИБКА ЗАПРОСА')
	
	try:
		os.makedirs(result_dir + '/' + link.directory, mode=0o777)
	except OSError:
		print('Директория ', result_dir + '/' + link.directory, ' существует')
	else:
		print('Директория ', result_dir + '/' + link.directory, ' создана')

	img_file = open(os.getcwd() + '/' + result_dir + '/' + link.directory + '/' + link.filename, 'wb')
	try:
		img_file.write(img.content)
	except OSError:
		print('Файл ' + link.url + ' НЕ УДАЛОСЬ СОХРАНИТЬ')
	else:
		print('Файл ' + link.url + ' СОХРАНЕН')
	img_file.close()
	time.sleep(0.1)

f_urls.close()


# img_url = 'https://dg-home.ru/pic/114470/kreslo_krugloe_sinee_s_podushkami_monroe_2__1.jpg'

