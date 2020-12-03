import logging
import collections
import re
import csv
import json
import time
from pprint import pprint
import os
# import cssutils
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%y%m%d-%H%M%S")

import requests
import bs4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')

class Client:
	ParseResult = {
		'source_url': '',
		'product_category': '',
		'product_category_chain': '',
		'product_name': '',
		'product_code': '',
		'product_price': '',
		'main_image' : '',
		'additional_images' : '',
		'product_params' : '',
		'product_description': ''
	}

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
			return res.text
		except requests.exceptions.HTTPError as error: 
			print(error)
			return False

	def parse_page(self, text: str):
		soup = bs4.BeautifulSoup(text, 'lxml')

		# Вызов функции парсинга категории
		container = soup.select('div.bx-breadcrumb')
		for block in container:
			self.product_category(block=block)

		# Вызов функции парсинга названия товара
		container = soup.select('h1')
		for block in container:
			self.parse_name(block=block)

		# Вызов функции парсинга артикула товара
		container = soup.select('h1')
		for block in container:
			self.parse_code(block=block)

		# Вызов функции парсинга цены
		container = soup.select('div.aa_e_price')
		for block in container:
			self.parse_price(block=block)

		# Вызов функции парсинга основной картинки
		container = soup.select('div.aa_e_img_bl')
		for block in container:
			self.parse_main_image(block=block)

		# Вызов функции парсинга доп. картинок
		container = soup.select('div.ok_e_nav_bl')
		for block in container:
			self.parse_additional_images(block=block)

		# Вызов функции парсинга свойств товара
		container = soup.select('div.aa_dtovall')
		for block in container:
			self.parse_params(block=block)

		# Вызов функции парсинга описания товара
		container = soup.select('div.aa_detailtov_opis')
		for block in container:
			self.parse_description(block=block)

	# Парсинг категории товара
	def product_category(self, block):
		category_tree = block.select('.bx-breadcrumb-item > a')
		last_item = None
		last_item = category_tree[len(category_tree)-1] or ''
		parent_item = category_tree[len(category_tree)-2] or ''
		product_category_chain = '['
		for last_item in category_tree:
			product_category_chain += '"%s",' % last_item.get_text().strip()
		product_category_chain += ']'
		# if last_item:
		product_category = '{ "name": "%s", "url": "%s", "parent_name": "%s", "parent_url": "%s" }' % ( last_item.get_text().strip(), last_item.get('href'), parent_item.get_text().strip(), parent_item.get('href') )

		self.ParseResult['product_category'] = product_category
		self.ParseResult['product_category_chain'] = product_category_chain

	# Парсинг названия товара
	def parse_name(self, block):
		self.ParseResult['product_name'] = '"%s"' % block.select_one('span').getText()

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
		discount_price_block = block.select_one('.ok_pr')
		if (discount_price_block): discount_price = discount_price_block.getText()
		else: discount_price = '0'

		full_price_block = block.select_one('.ok_pr_disc')
		if (full_price_block): full_price = full_price_block.getText()
		else: full_price = '0'

		full_price = re.sub(r'тг.', '', full_price)
		full_price = int(re.sub(r'\s*', '', full_price))
		discount_price = re.sub(r'тг.', '', discount_price)
		discount_price = int(re.sub(r'\s*', '', discount_price))

		self.ParseResult['product_price'] = '{ "full" : %s, "discounted": %s }' % (max(full_price, discount_price), min(full_price, discount_price))

	# Парсинг основной картинки товара
	def parse_main_image(self, block):
		image_block = block.select_one('a.aa_e_img')
		if not image_block:
			logger.error('not url block')
			# return

		main_image_url = image_block.get('href')

		if not main_image_url:
			logger.error('no href')
			# return

		if (main_image_url):
			try:
					main_image = '{ "url": "%s", "alt": "%s" }' % ( main_image_url, image_block.get('title') or '' )
			except:
					main_image = '{ "url": "%s", "alt": "%s" }' % ( '', '' )

		# logger.debug(main_image)
		self.ParseResult['main_image'] = main_image

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
		# print(product_params)
		# product_params = re.sub(r',\s*}', '}', product_params)
		# product_params = re.sub(r',\s*$', '', product_params)
		
		self.ParseResult['product_params'] = product_params

	def parse_description(self, block):
		rows = block.select('div.aa_marketing')
		content = ''
		for row in rows:
			content += row.decode_contents()
		content = re.sub(r'\s+', ' ', content)

		images_img = re.findall(r'<img.*src\s*=\s*[\"\'](.*?)[\"\']', content)
		images_bg = re.findall(r'url\([\'\"\ ]?(.*?)[\'\"\ ]?\)', content)
		images_arr = images_bg + images_img
		images = ''
		for image in images_arr:
			images += '{ "url": "%s", "alt": %s }, ' % (image, self.ParseResult['product_name'])
		# images = '"' + '", "'.join(images_bg + images_img) + '"'
		
		product_description = '{ "content": "%s", "images": [%s] }' % ( re.sub(r'"', '\\"', content), images)
		self.ParseResult['product_description'] = product_description

	def run(self):
		logger.debug('='*50)
		text = self.load_page()
		if not text: return False
		self.parse_page(text=text)
		self.save_result()

	def save_result(self):
		self.ParseResult['source_url'] = '"%s"' % self.url
		path = self.result_file_path
		with open(path, 'w', encoding='utf-8') as f:
			result = '{\n'
			# f.write('{\n')
			for i, key in enumerate(self.ParseResult):
				result += ( '"%s": %s%s,\n' % (key, self.ParseResult[key], '' if i == len(self.ParseResult)-1 else ', ') ) 
			result += ('\n}, \n')

			result = re.sub(r',\s*]', ']', result)
			result = re.sub(r',\s*}', '}', result)
			result = re.sub(r',\s*$', '', result)
			result = re.sub(r',\s*,', ',', result)

			try:
				f.write(json.dumps(json.loads(result), indent=2, sort_keys=False, ensure_ascii=False))
			except:
				f.write(result)

if __name__ == '__main__':
	source_file_path = 'product-urls.txt'
	result_file_path = 'result.json'
	result_folder = 'result-'+ current_time + '/'
	start_index = 0
	end_index = 10000

	if not os.path.isdir(result_folder):
		os.mkdir(result_folder)

	counter = 0
	with open(source_file_path, 'r', encoding='utf-8') as f:
		while True:
			counter += 1
			url = f.readline().strip()
			if counter < start_index: continue
			if counter > end_index: break
			if len(url) == 0: break
			parser = Client(url, result_folder + f'{counter:05d}' + '-' + result_file_path)
			print(f'{counter:05d}')
			print(url)
			parser.run()
			time.sleep(1)
