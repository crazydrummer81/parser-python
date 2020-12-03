import logging
import collections
import re
import csv
import json
import time
from os import mkdir
from os import remove
# from sys import exit
from datetime import datetime

import requests
import bs4

now = datetime.now()
current_time = now.strftime("%y%m%d-%H0000")
print("Current Time =", current_time)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')

CATEGORIES = set()
CAT_IMGS_DICT = {}
PARENT_COUNT = 0

class Client:

	ParseResult = {
		'product_category_chain': '',
	}

	def __init__(self, url, result_file_path):
		# Запитывает в себя куки, заголовки и т.д., чтобы не заподозрили
		self.session = requests.session()
		self.session.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
			"Accept-Language": "ru",
		}
		self.url = url
		self.result_file_path = result_file_path

	def load_page(self):
		url = self.url
		res = self.session.get(url=url)
		try:
			res.raise_for_status()
			return res.text
		except requests.exceptions.HTTPError as error:
			print(error)
			return False

	def parse_page(self, text: str):
		soup = bs4.BeautifulSoup(text, 'lxml')

		container = soup.select('div.bx-breadcrumb')
		for block in container:
			self.parse_category(block=block)

	def parse_category(self, block):
		# product_categories_tree = block.select('div.breadcrumbs__insideItem')
		global PARENT_COUNT
		# Парсим всю цепочку категорий
		items = block.select('div.bx-breadcrumb-item a')
		product_category_chain = ''
		for item in items:
			title = item.get('title').strip()
			# if title:
			# 	#todo Найти соответствие категории в файле с привязкой картинок к категориям
			# 	#todo Если есть, добавить в [] url картинки
			# 	cat_image = ''
			# 	for i, cat in enumerate(CAT_IMGS_DICT):
			# 		if cat['category_name'].strip() == title:
			# 			print(cat['category_name'])
			# 			cat_image = cat['category_image']
			# 			PARENT_COUNT += 1
			# 			print(PARENT_COUNT)
			# 			break
				# product_category_chain += title + '[' + cat_image + ']/'
				product_category_chain += title + '^'
		# product_category_chain = '%s' % product_category_chain
		# print(product_category_chain)
		self.ParseResult['product_category_chain'] = product_category_chain

	def save_result(self):
		CATEGORIES.add(self.ParseResult['product_category_chain'])

	def run(self):
		text = self.load_page()
		if not text:
			return False
		self.parse_page(text=text)
		self.save_result()


if __name__ == '__main__':
	result_file_path = 'stanki.json'
	source_file_path = 'brands-urls-2.txt'
	result_folder = 'categories-chain-' + current_time + '/'
	categories_path = 'categories.txt'

	# достаем из файла с привязкой категорий с картинками и записываем в массив
	cat_imgs_path = 'categories-200901-170000/categories.json'
	with open(cat_imgs_path, 'r',encoding='utf-8') as f:
		CAT_IMGS_DICT = json.load(f)
	
	start_index = 0
	end_index = 500

	try:
		mkdir(result_folder)
	except:
		print("FORDER EXISTS")
		# exit("FORDER EXISTS")

	#remove(result_folder + categories_path)
	counter = 0
	with open(source_file_path, 'r', encoding='utf-8') as f:
		while True:
			counter += 1
			url = f.readline().strip()
			if counter < start_index:
					continue
			if counter > end_index:
					break
			if len(url) == 0:
					break
			parser = Client(url, result_folder +
									f'{counter:05d}' + '-' + result_file_path)
			print(f'{counter:05d}')
			print(url)
			parser.run()
			cat_str = '/'.join(CATEGORIES)
			# cat_str = '####'.join([re.sub('"', "", item) for item in CATEGORIES])
			with open(result_folder + categories_path, 'w', encoding='utf-8') as fc:
					[fc.write(cat_str + '\n') for cat_str in CATEGORIES]
			# print(CATEGORIES)
			time.sleep(.1)
