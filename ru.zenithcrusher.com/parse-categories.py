import logging
import collections
import re
import csv
import json
import time
from pprint import pprint
from os import mkdir
# import cssutils
from datetime import datetime

import requests
import bs4

#todo Спарсить все ссылки на погрузчики

#! БЛОКИ НА ПАРСИНГ:
#! - Названия катекории
#! - Описание категории
#! - Фото категории
#! - url категории

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')

now = datetime.now()
current_time = now.strftime("%y%m%d-%H0000")
print('TIME: ' + current_time)

class Client:
	ParseResult = []

	result_file_path = ''

	def __init__(self, url, result_file_path):
		self.session = requests.session() # Запитывает в себя куки, заголовки и т.д., чтобы не заподозрили
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
			res.encoding = 'utf8'
			return res.text
		except requests.exceptions.HTTPError as error: 
			print(error)
			return False

	def parse_page(self, text: str):
		soup = bs4.BeautifulSoup(text, 'lxml')

		#! Вызов функции парсинга Названия катекории
		container = soup.select('div.mainBox')
		for block in container:
			self.categoty_name(block=block)

	# Парсинг категории товара
	def categoty_name(self, block):
		cards = block.select('div.eachBox')
		if cards:
			for card in cards:
				card_dict = {}
				card_dict['categoty_image'] = card.select_one('img').get('src')
				card_dict['categoty_name'] = card.select_one('h2>a').getText()
				card_dict['categoty_url'] = card.select_one('h2>a').get('href')
				card_dict['categoty_detail_text'] = card.select_one('p').getText()
				# print(card_dict['categoty_detail_text'])
				self.ParseResult.append(card_dict)
		else:
			print('NO CATEGORIES CARDS')

	def run(self):
		logger.debug('='*50)
		text = self.load_page()
		if not text: return False
		self.parse_page(text=text)
		self.save_result()

	def save_result(self):
		# self.ParseResult['source_url'] = '"%s"' % self.url
		# print(self.ParseResult)

		with open(self.result_file_path, 'w', encoding='utf-8') as f:
			try:
				f.write(json.dumps(self.ParseResult, indent=2, sort_keys=False, ensure_ascii=False))
			except:
				print('Error write to file...')

if __name__ == '__main__':
	# source_file_path = 'products-urls.txt'
	result_file_path = 'result.json'
	result_folder = 'categories-' + current_time + '/'
	start_index = 0
	end_index = 2000

	try:
		mkdir(result_folder)
	except:
		print('FODER EXISTS')

	# counter = 0
	# with open(source_file_path, 'r', encoding='utf-8') as f:
	# 	while True:
	# 		counter += 1
	url = 'https://ru.zenithcrusher.com/products/'
	# if counter < start_index: continue
	# if counter > end_index: break
	# if len(url) == 0: break
	parser = Client(url, result_folder + result_file_path)
	# print(f'{counter:05d}')
	print(url)
	parser.run()
	# time.sleep(1)
