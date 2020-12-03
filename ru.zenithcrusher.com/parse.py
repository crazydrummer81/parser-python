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
from selenium import webdriver
chomedriver_path = 'chromedriver.exe'
driver = webdriver.Chrome(chomedriver_path)



#todo Спарсить все ссылки на погрузчики

#! БЛОКИ НА ПАРСИНГ:
#! Категория
#! Главное фото
#! Описание
#! Цена
#! Характеристики HTML

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')

now = datetime.now()
current_time = now.strftime("%y%m%d-%H0000")
print('TIME: ' + current_time)

class Client:
	ParseResult = {
		'source_url': None,
		'product_category_chain': None,
		'product_name': None,
		# 'product_price': None,
		'pruduct_detail_image' : None,
		# 'additional_images' : None,
		'product_characteristics_html' : None,
		'product_detail_text': None,
		'product_preview_text': None,
	}

	result_file_path = ''

	def __init__(self, url, result_file_path):
		# self.session = requests.session() # Запитывает в себя куки, заголовки и т.д., чтобы не заподозрили
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

		#! Вызов функции парсинга цепочки категории
		container = soup.select('div.menuNavin')
		for block in container:
			self.product_category(block=block)

		#! Вызов функции парсинга названия товара
		container = soup.select('div.content h1')
		for block in container:
			self.parse_name(block=block)

		#! Вызов функции парсинга артикула товара
		# container = soup.select('h1')
		# for block in container:
		# 	self.parse_code(block=block)

		#! Вызов функции парсинга цены
		# container = soup.select('p.card__request')
		# for block in container:
		# 	self.parse_price(block=block)

		#! Вызов функции парсинга основной картинки
		container = soup.select('div.mainBox .proPic')
		for block in container:
			self.parse_main_image(block=block)

		#! Вызов функции парсинга доп. картинок
		# container = soup.select('div.ok_e_nav_bl')
		# for block in container:
		# 	self.parse_additional_images(block=block)

		#! Вызов функции парсинга свойств товара (с помощью selenuim)
		driver.get(self.url)
		try:
			container = driver.find_element_by_css_selector('table.para_table').get_attribute('outerHTML')
			if container:
				self.parse_characteristics(block = driver.find_element_by_css_selector('table.para_table').get_attribute('outerHTML'))
		except:
			'Нет характеристик в отдельном табе...'

		#! Вызов функции парсинга описания товара
		container = soup.select('div.mainBox')
		for block in container:
			self.parse_description(block=block)

		#! Вызов функции парсинга краткого описания товара
		container = soup.select('div.proAbout')
		for block in container:
			self.parse_description_short(block=block)

	# Парсинг цепочки категории товара
	def product_category(self, block):
		category_tree = block.select('a')
		chain = []
		for item in category_tree:
			chain.append({'name' : re.sub(r'[^a-zA-Zа-яА-Я]+', '', item.getText()), 'url': item.get('href')})
		self.ParseResult['product_category_chain'] = chain

	# Парсинг названия товара
	def parse_name(self, block):
		self.ParseResult['product_name'] = block.getText()

	# Парсинг артикула товара
	def parse_code(self, block):
		pprint(block.select_one('span.element-article'))
		try:
			product_code = block.select_one('span.element-article').getText()
		except:
			product_code = ''
			logger.error('ERROR PARSING CODE')

		product_code = '"%s"' % product_code
		product_code = re.sub(r'Код:\s*', '', product_code)
		self.ParseResult['product_code'] = product_code

	# Порсинг цен товара
	def parse_price(self, block):
		full_price = block.getText()
		try:
			full_price = int(full_price)
		except:
			full_price = '""'
		discount_price = '""'

		self.ParseResult['product_price'] = '{ "full" : %s, "discounted": %s }' % (max(full_price, discount_price), min(full_price, discount_price))

	# Парсинг основной картинки товара
	def parse_main_image(self, block):
		image_block = block.select_one('img')
		if not image_block:
			logger.error('not url block')
			# return

		try:
			main_image_url = image_block.get('src')
		except:
			main_image_url = ''
		# print(main_image_url)

		if not main_image_url:
			logger.error('no src')
			# return

		try:
				main_image = {
					'url': re.sub(r'\/*(https?:\/*)?static.zenithcrusher.com', '', main_image_url), 
					'alt': image_block.get('alt') or '' 
				}
		except:
				main_image = { 'url': '', 'alt': '' }

		# logger.debug(main_image)
		self.ParseResult['pruduct_detail_image'] = main_image['url']
		self.ParseResult['main_image'] = main_image

	# Парсинг доп. картинок товара
	def parse_additional_images(self, block):
		images_blocks = block.select('a')
		additional_images = '[ '
		for image_block in images_blocks:
			image_alt = image_block.get('alt')
			image_url = image_block.select_one('img').get('src')
			additional_images += '{ "url": "%s", "alt": "%s" }, ' % (image_url, image_alt)
		additional_images += ' ]'
		self.ParseResult['additional_images'] = additional_images

	# Парсинг свойств товара
	def parse_params(self, block):
		# for i, params_column in enumerate(block):
		# product_params = '{ '
		product_params = '{'
		params_lines = block.select('div')
		for i, line in enumerate(params_lines):
			if(line['class'][0] == 'aa_dtprop_h'): # Заголовок свойства
				product_params += '"%s" : { ' % line.getText()
			if(line['class'][0] == 'aa_dtpropname'): # Название свойства
				product_params += ' "%s": ' % re.sub(r':\s*$', '', line.getText())
			if(line['class'][0] == 'aa_dtpropval'): # Значение свойства
				product_params += '"%s", ' % line.getText()
			if ( i < len(params_lines)-1 ):
				if( (params_lines[i+1]['class'][0] == 'aa_dtprop_h') and (i > 0) ):
					product_params += ' }, '
		product_params += ' } } '
		
		self.ParseResult['product_params'] = product_params

	# Парсинг описания товара
	def parse_description(self, block):

		tabs = block.select('div.eachInfo')
		if tabs:	
			tab1 = re.sub(r'\s+', ' ', tabs[0].decode_contents()) or ''
			tab2 = re.sub(r'\s+', ' ', tabs[1].decode_contents()) or ''
		else:
			tab1, tab2 = '', ''
		
		more_content = block.select_one('div.crushingPlant')
		# print('MPORE CONTENT', more_content)
		if more_content:
			print('IF MORE CONTENT',type(more_content))
			children = more_content.select('*')
			# print('CHILDREN:', children)
			for child in children:
				# print(child.name)
				if child.name == 'table':
					tab2 += child.decode_contents()
				else:
					tab1 += child.decode_contents()
	
		images_img = re.findall(r'<img.*src\s*=\s*[\"\'](.*?)[\"\']', tab1 + tab2)
		images_bg = re.findall(r'url\([\'\"\ ]?(.*?)[\'\"\ ]?\)', tab1 + tab2)
		images_arr = images_bg + images_img
		images = []
		for image in images_arr:
			images.append({ "url": image, "alt": self.ParseResult['product_name'] })
		product_detail_text = {
			"description": tab1,
			# "characteristics": re.sub(r'<script.*?\/script>', '', tab2),
			"images": images 
		}
		self.ParseResult['product_detail_text'] = product_detail_text['description']
		self.ParseResult['product_detail_text_images'] = product_detail_text['images']
		self.ParseResult['product_characteristics_html'] = re.sub(r'\s+', ' ', tab2)
	
	def parse_characteristics(self, block):
		self.ParseResult['product_characteristics_html'] = re.sub(r'\s+', ' ', block)

	def parse_description_short(self, block):

		content = block.select_one('div.proText').decode_contents()
		content = re.sub(r'\s+', ' ', content)

		self.ParseResult['product_preview_text'] = content

	def run(self):
		logger.debug('='*50)
		text = self.load_page()
		if not text: return False
		self.parse_page(text=text)
		self.save_result()

	def save_result(self):
		self.ParseResult['source_url'] = self.url
		path = self.result_file_path
		# print(self.ParseResult)

		with open(path, 'w', encoding='utf-8') as f:
			try:
				f.write(json.dumps(self.ParseResult, indent=2, sort_keys=False, ensure_ascii=False))
			except Exception as e:
				print(e)

if __name__ == '__main__':
	# Берем json из файла и загоняем в словарь
	source_file_path = 'source/product-links-all.txt'
	with open(source_file_path, 'r', encoding='utf-8') as f:
		pages = f.readlines()

	result_file_path = 'result.json'
	result_folder = 'result-' + current_time + '/'
	start_index = 0
	end_index = 100000
	try:
		mkdir(result_folder)
	except:
		print('FODER EXISTS')

	for counter, url in enumerate(pages):
		if counter < start_index: continue
		if counter > end_index: break
		parser = Client(url.strip(), result_folder + f'{counter:05d}' + '-' + result_file_path)
		print(f'{counter:05d}')
		print(url)
		parser.run()
		time.sleep(0.1)
