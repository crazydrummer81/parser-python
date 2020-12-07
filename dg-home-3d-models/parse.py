import logging
import collections
import re
import csv
import json
import time
from pprint import pprint
from os import mkdir
from os import listdir
# import cssutils
from datetime import datetime
from time import sleep

import requests
import bs4
from selenium import webdriver
# chomedriver_path = 'D:\Distr\Coding\Parsing\geckodriver.exe'

# получаем список имен скачанных файлов
dl_files_list = listdir('./download/')
# вытаскиваем от туда артикулы
dl_sku_list = [re.search(r'арт_(.*?)\.zip',item).group(1) for item in dl_files_list]
print('ITEMS: %s' % len(dl_sku_list))

if not False:
	firefox_profile = webdriver.FirefoxProfile()
	firefox_profile.set_preference('permissions.default.image', 2)
	firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
	driver = webdriver.Firefox(firefox_profile=firefox_profile)
	# driver = webdriver.Firefox()

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
		'product_price': None,
		'pruduct_detail_image' : None,
		'additional_images' : None,
		'product_characteristics' : [],
		'product_detail_text': None,
		'product_preview_text': None,
	}
	isClicked = False

	result_file_path = ''

	def __init__(self, url, result_file_path):
		# self.session = requests.session() # Запитывает в себя куки, заголовки и т.д., чтобы не заподозрили
		# self.session = requests.session() # Запитывает в себя куки, заголовки и т.д., чтобы не заподозрили
		# self.session.headers = {
		# 	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
		# 	"Accept-Language": "ru",
		# }
		self.url = url
		self.result_file_path = result_file_path


	def load_page(self):
		driver.get(url)

	def parse_page(self, text = ''):
		# print('parse_page()')

		#! Вызов функции парсинга цепочки категории
		self.product_category()
		self.parse_name()
		self.parse_code()
		self.parse_price()
		self.parse_images()
		self.parse_params()
		self.parse_description()
		self.parse_description_short()
		self.click3d()

	# Парсинг цепочки категории товара
	def product_category(self):
		# print('product_category()')
		category_tree = driver.find_elements_by_css_selector('.main__breadcrumbs .ul-wrap ul li[itemprop=itemListElement] a')

		chain = []
		for item in category_tree:
			name = re.sub(r'[^a-zA-Zа-яА-Я]+', '', item.text)
			url = item.get_attribute('href')
			chain.append({'name' : name, 'url': url})
		self.ParseResult['product_category_chain'] = chain
		# print('chain', chain)

	# Парсинг названия товара
	def parse_name(self):
		name_node = driver.find_element_by_css_selector('.maininfo--title')
		name = name_node.get_attribute('innerText').strip()
		# print('name', name)
		self.ParseResult['product_name'] = name

	# Парсинг артикула товара
	def parse_code(self):
		sku_node = driver.find_element_by_css_selector('span[itemprop=sku]')
		self.ParseResult['product_code'] = sku_node.get_attribute('innerText').strip()
		# print('sku', sku_node.get_attribute('innerText').strip())

	# Порсинг цен товара
	def parse_price(self):
		# try:
		# 	price_node = driver.find_element_by_css_selector('.sale-price')
		# except:
		# 	print('no .sale-price')
		try:
			new_price_node = driver.find_element_by_css_selector('.new-price')
		except:
			print('no .new-price')
			new_price_node = False
		try:
			old_price_node = driver.find_element_by_css_selector('.new-price-bottom')
		except:
			print('no .new-price-bottom')
			old_price_node = False

		new_price = re.sub(r'\s*', '', new_price_node.text or '') if new_price_node else 0
		old_price = re.sub(r'\s*', '', old_price_node.text or '') if old_price_node else 0

		self.ParseResult['product_price'] = {'new_price': int(new_price), 'old_price': int(old_price)}
		# print('price', self.ParseResult['product_price'])

	# Парсинг основной картинки товара
	def parse_images(self):
		slider_node = driver.find_element_by_css_selector('.slideshow')
		slide_nodes = slider_node.find_elements_by_css_selector(':scope > div')
		# print(slide_nodes[0].get_attribute('innerHTML'))

		slider_arr = []
		i = 0
		for slide in slide_nodes:
			# print('img: %s' % i)
			try:
				src = slide.get_attribute('data-image')
				# print('SRC', src)
				if (src): slider_arr.append(src)
			except:
				print('NO IMG')
			i += 1

		self.ParseResult['pruduct_detail_image'] = slider_arr[0]
		self.ParseResult['additional_images'] = slider_arr[1:]

	# Парсинг свойств товара
	def parse_params(self):
		product_characteristics = []
		descr_tabs_nodes = driver.find_elements_by_css_selector('.desc-tabs--content')
		for tab_node in descr_tabs_nodes:
			# Находим из всех вкладок ту, для которй есть название "Характеристики"
			header_node = tab_node.find_element_by_css_selector('.desc-tabs--content-title')
			if 'характеристики' in header_node.get_attribute('innerText').strip().lower():
				# В найденной владке вытаскиваем свойства
				prop_nodes = tab_node.find_elements_by_css_selector('.chars-item')
				for prop_node in prop_nodes:
					key = prop_node.find_element_by_css_selector('.chars-item--field').get_attribute('innerText').strip()
					key = re.sub(r'\s*:', '', key)
					value = prop_node.find_element_by_css_selector('.chars-item--right').get_attribute('innerText').strip()
					product_characteristics.append({key: value})

		self.ParseResult['product_characteristics'] = product_characteristics

	# Парсинг описания товара
	def parse_description(self):
		descr_html = ''
		descr_tabs_nodes = driver.find_elements_by_css_selector('.desc-tabs--content')
		for tab_node in descr_tabs_nodes:
			# Находим из всех вкладок ту, для которй есть название "Описание"
			header_node = tab_node.find_element_by_css_selector('.desc-tabs--content-title')
			# print('header_node.text.lower()', header_node.get_attribute('innerText').strip().lower())
			if 'описание' in header_node.get_attribute('innerText').strip().lower():
				# В найденной владке вытаскиваем HTML
				descr_html = tab_node.get_attribute('innerHTML')
	
		images_img = re.findall(r'<img.*src\s*=\s*[\"\'](.*?)[\"\']', descr_html)
		images_bg = re.findall(r'url\([\'\"\ ]?(.*?)[\'\"\ ]?\)', descr_html)
		images_arr = images_bg + images_img
		images = []
		for image in images_arr:
			images.append({ "url": image, "alt": self.ParseResult['product_name'] })

		self.ParseResult['product_detail_text'] = descr_html
		self.ParseResult['product_detail_text_images'] = images
	
	def parse_description_short(self):
		content = ''
		self.ParseResult['product_preview_text'] = content

	def click3d(self):
		driver.execute_script("const a123 = document.querySelector('.q-panel'); if(a123) a123.style.display = 'none';")
		driver.execute_script("const b123 = document.querySelector('.modalBuilder'); if (b123) b123.style.display = 'none';")
		
		try:
			link = driver.find_element_by_css_selector('.main-buttons--subscrb-link-3')
		except:
			print('no .main-buttons--subscrb-link-3')
			link = None
			return
		link.click()
		self.isClicked = link != None
		# sleep(1)

	def run(self):
		logger.debug('='*50)
		self.load_page()
		self.parse_page()
		self.save_result()
		return self.isClicked

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
	user_login = 'mamirov3d+dg-home.ru-001@gmail.com'
	user_psw = 'xbQI7240'
	source_file_path = 'product-pages-urls.json'
	with open(source_file_path, 'r', encoding='utf-8') as f:
		pages = json.load(f)
	# print(pages)

	if not False:
		# Логинимся по первой ссылке
		driver.get(pages[0])
		login_button = driver.find_element_by_css_selector("a.sing_in")
		login_button.click()
		input_login = driver.find_element_by_css_selector("input[name=USER_LOGIN]")
		input_login.send_keys(user_login)
		input_psw = driver.find_element_by_css_selector("input[name=USER_PASSWORD]")
		input_psw.send_keys(user_psw)
		form = driver.find_element_by_css_selector("form.popup-form.popup-form-login")
		form.submit()
		print('Login to site and enter something to continue: ')
		a123 = input()

	# вытаскиваем ссылки на продукты со страниц массива
	if False:
		categories_urls_file_path = 'product-pages-urls.json'
		result_folder = 'result-' + current_time + '/'
		start_index = 90
		end_index = 270
		try:
			mkdir(result_folder)
		except:
			print('FODER EXISTS')


	if False:
		# Парсим ссылки на целевые страницы со страниц категорий 
		product_urls = []
		start_index = 0
		end_index = 20000
		for counter, url in enumerate(pages):
			driver.get(url)
			if counter < start_index: continue
			if counter > end_index: break
			product_urls_nodes = driver.find_elements_by_css_selector('.q-product__item a')

			print('Page: ', counter)
			for node in product_urls_nodes:
				href = node.get_attribute('href')
				if (not (href in product_urls) and (href)): product_urls.append(href)

		with open(categories_urls_file_path, 'w', encoding='utf-8') as f:
				try:
					f.write(json.dumps(product_urls, indent=2, sort_keys=False, ensure_ascii=False))
				except Exception as e:
					print(e)

	result_file_path = 'result.json'
	# result_folder = 'result-' + current_time + '/'
	result_folder = 'result-final/'
	start_index = 0
	end_index = 2000
	max_clicks = 130
	try:
		mkdir(result_folder)
	except:
		print('FODER EXISTS')

	count_allready_dl = 0
	count3d = 0
	for counter, url in enumerate(pages):
		if counter < start_index: continue
		if counter > end_index: break

		#todo СВЕРИТЬ JSON-ФАЙЛ И СКАЧАНЫЕ ФАЙЛЫ, ЕСЛИ ФАЙЛ СКАЧАН, ПРОПУСКЕМ
		target_filename = result_folder + f'{counter:05d}' + '-' + result_file_path
		try:
			with open(target_filename, 'r', encoding='utf-8') as f:
				product = json.load(f)
			print(product['product_code'])
			if f and (product['product_code'] in dl_sku_list): 
				count_allready_dl += 1
				print('3D-модель продукта %s скачана.\nСкачано %s моделей.' % (product['product_code'], count_allready_dl))
				continue
		except:
			print ('Файла %s не существует пока' % target_filename)
		

		parser = Client(url.strip(), target_filename)
		sleep(2)
		print(f'---> {counter:05d} <---')
		print(url)
		if (parser.run()): count3d += 1
		print('CLICKED: %s' % count3d)
		if count3d > max_clicks:
			print('Прокликано %s ссылок. Пока остановимся...' % max_clicks)
			break
		sleep(0.1)
