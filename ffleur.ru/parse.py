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
from translit import transliterate

import requests
import bs4
from selenium import webdriver
webdriver_path = 'D:\Distr\Coding\Webdriver\geckodriver.exe'

# получаем список имен скачанных файлов
dl_files_list = listdir('./download/')
# вытаскиваем от туда артикулы
dl_sku_list = [re.search(r'арт_(.*?)\.zip',item).group(1).strip() for item in dl_files_list]
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
	ParseResult = {}
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
		# if url: driver.get(url)
		pass

	def parse_page(self, text = ''):
		# print('parse_page()')

		#! Вызов функции парсинга цепочки категории
		self.product_category() # Done
		self.parse_name() # Done
		self.parse_id() # Done
		# self.parse_code()
		self.parse_price() # Done
		self.parse_images() # Done
		self.parse_params() # Done
		self.parse_description() # Done
		self.parse_description_short() # Done
		self.parse_variant_image() # Done
		self.parse_accessories_ids() # Done
		self.parse_related_ids() # Done
		# self.click3d()

	# Парсинг цепочки категории товара
	def product_category(self):
		# print('product_category()')
		category_tree = driver.find_elements_by_css_selector('#breadcrumbs a[itemprop="url"]')

		chain = []
		for item in category_tree:
			name = re.sub(r'[^a-zA-Zа-яА-Я ]+', '', item.get_attribute('innerText')).strip()
			url = item.get_attribute('href')
			chain.append({'name' : name, 'url': url})
		self.ParseResult['category_chain'] = chain
		# print('chain', chain)

	# Парсинг названия товара
	def parse_name(self):
		name_node = driver.find_element_by_css_selector('h1')
		name = name_node.get_attribute('innerText').strip()
		# print('name', name)
		self.ParseResult['name'] = name

	# Парсинг артикула товара
	def parse_code(self):
		sku_node = driver.find_element_by_css_selector('span[itemprop=sku]')
		self.ParseResult['code'] = sku_node.get_attribute('innerText').strip()
		# print('sku', sku_node.get_attribute('innerText').strip())

	# Парсинг внутреннего ID товара
	def parse_id(self):
		id_node = driver.find_element_by_css_selector('#catalogElement ')
		self.ParseResult['id'] = id_node.get_attribute('data-product-id').strip()
		# print('id', id_node.get_attribute('data-product-id').strip())

	# Порсинг цен товара
	def parse_price(self):
		# try:
		# 	price_node = driver.find_element_by_css_selector('.sale-price')
		# except:
		# 	print('no .sale-price')
		# try:
		# 	new_price_node = driver.find_element_by_css_selector('#catalogElement .priceVal')
		# except:
		# 	print('no .priceVal')
		# 	new_price_node = False
		new_price_node = False
		try:
			old_price_node = driver.find_element_by_css_selector('#catalogElement .priceVal')
		except:
			print('no .priceVal')
			old_price_node = False

		new_price = re.sub(r'\D', '', new_price_node.get_attribute('textContent') or '') if new_price_node else 0
		old_price = re.sub(r'\D', '', old_price_node.get_attribute('textContent') or '') if old_price_node else 0

		self.ParseResult['price'] = {'new_price': int(new_price), 'old_price': int(old_price)}
		# print('price', self.ParseResult['price'])

	# Парсинг основной картинки товара
	def parse_images(self):
		slider_node = driver.find_element_by_css_selector('#catalogElement .pictureSlider')
		slide_nodes = slider_node.find_elements_by_css_selector(':scope > div a.zoom')
		# print(slide_nodes[0].get_attribute('innerHTML'))

		slider_arr = []
		i = 0
		for slide in slide_nodes:
			# print('img: %s' % i)
			try:
				src = slide.get_attribute('href')
				# print('SRC', src)
				if (src): slider_arr.append(src)
			except:
				print('NO IMG')
			i += 1

		self.ParseResult['detail_image'] = slider_arr[0]
		self.ParseResult['additional_images'] = slider_arr[1:]

	# Парсинг свойств товара
	def parse_params(self):
		product_characteristics = {}
		props_wrapper_node = driver.find_element_by_css_selector('#catalogElement .detailPropertiesTable table')
		# prop_group_nodes = props_wrapper_node.find_elements_by_css_selector('tr.cap')
		prop_nodes = props_wrapper_node.find_elements_by_css_selector('tr')

		result = {}
		props_group_name = 'default'
		for prop_node in prop_nodes:
			if 'cap' in prop_node.get_attribute('class'):
				props_group_name = prop_node.get_attribute('textContent').strip()
				result[props_group_name] = {}
			else:
				row_node = prop_node.find_elements_by_css_selector('td')
				key = row_node[0].get_attribute('textContent').strip()
				value = row_node[1].get_attribute('textContent').strip()
				result[props_group_name][key] = value

		self.ParseResult['characteristics'] = result

	# Парсинг описания товара
	def parse_description(self):
		descr_html = ''
		try:
			descr_node = driver.find_element_by_css_selector('#detailText .changeDescription')
			go = True
		except:
			print('NO #detailText .changeDescription')
			go = False

		if go:
			descr_html = descr_node.get_attribute('innerHTML')
		
			images_img = re.findall(r'<img.*src\s*=\s*[\"\'](.*?)[\"\']', descr_html)
			images_bg = re.findall(r'url\([\'\"\ ]?(.*?)[\'\"\ ]?\)', descr_html)
			descr_html = re.sub(r'\s+', ' ', descr_html).strip() #! Не тестировал
			images_arr = images_bg + images_img
			images = []
			for image in images_arr:
				images.append({ "url": image, "alt": self.ParseResult['name'] })
		else:
			descr_html = ''
			images = []

		self.ParseResult['detail_text'] = descr_html
		self.ParseResult['detail_text_images'] = images
	
	def parse_description_short(self):
		try:
			node = driver.find_element_by_css_selector('#catalogElement .changeShortDescription')
			content = node.get_attribute('innerHTML')
		except:
			print('NO #catalogElement .changeShortDescription')
			content = ''
		self.ParseResult['preview_text'] = content

	def parse_variant_image(self):
		try:
			node = driver.find_element_by_css_selector('#catalogElement .elementSkuPropertyValue.selected a img')
			variant_image = node.get_attribute('src')
		except:
			print('NO #catalogElement .elementSkuPropertyValue.selected a img')
			variant_image = ''

		self.ParseResult['variant_image'] = variant_image

	def parse_accessories_ids(self):
		nodes = driver.find_elements_by_css_selector('#related .item')
		ids = []
		for node in nodes:
			pid = node.get_attribute('data-product-id')
			ids.append(pid)

		self.ParseResult['accessories_ids'] = ids

	def parse_related_ids(self):
		nodes = driver.find_elements_by_css_selector('#similar .item')
		ids = []
		for node in nodes:
			pid = node.get_attribute('data-product-id')
			ids.append(pid)

		self.ParseResult['related_ids'] = ids

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

	categories_urls_file_path = 'categories-pages-urls.json'
	products_urls_file_path = 'product-pages-urls.json'

	# Берем json из файла и загоняем в словарь
	user_login = 'mamirov3d+dg-home.ru-003@gmail.com'
	user_psw = 'xbQI7240'
	source_file_path = products_urls_file_path
	with open(source_file_path, 'r', encoding='utf-8') as f:
		pages = json.load(f)
	# print(pages)

	if False:
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
		result_folder = 'result-' + current_time + '/'
		start_index = 90
		end_index = 270
		try:
			mkdir(result_folder)
		except:
			print('FODER EXISTS')


	if False:
		# Парсим ссылки на целевые страницы со страниц категорий 
		base_url = 'http://ffleur.ru'
		url_params = [
			'SORT_TO=90' # Элементов на странице
		]

		source_file_path = categories_urls_file_path
		with open(source_file_path, 'r', encoding='utf-8') as f:
			pages = json.load(f)

		product_urls = []
		start_index = 0
		end_index = 20000
		for counter, raw_url in enumerate(pages):
			url = "%s%s?%s" % (base_url, raw_url, '&'.join(url_params))
			print(url)
			driver.get(url)
			if counter < start_index: continue
			if counter > end_index: break
			product_urls_nodes = driver.find_elements_by_css_selector('.productColImage a')

			print('Page: ', counter)
			for node in product_urls_nodes:
				href = node.get_attribute('href')
				if (not (href in product_urls) and (href)): product_urls.append(href)

			with open(products_urls_file_path, 'w', encoding='utf-8') as f:
					try:
						f.write(json.dumps(product_urls, indent=2, sort_keys=False, ensure_ascii=False))
					except Exception as e:
						print(e)
		print('EXIT...')
		exit()

	result_file_path = 'result.json'
	result_folder = 'result-' + current_time + '/'
	# result_folder = 'result-final/'
	start_index = 0
	end_index = 10000
	try:
		mkdir(result_folder)
	except:
		print('FODER EXISTS')


	# Выбираем город, чтобы далее не выскакивало
	driver.get('http://ffleur.ru')
	sleep(3)
	node = driver.find_element_by_css_selector('.geo-location-window-container')
	unput_node = node.find_element_by_css_selector('input')
	unput_node.send_keys('Москва')
	sleep(3)
	a_node = node.find_element_by_css_selector('.geo-location-list-item-link')
	a_node.click()
	sleep(1)
	a_node = node.find_element_by_css_selector('.geo-location-window-button')
	a_node.click()
	sleep(1)

	inner_counter = 0
	for counter, url in enumerate(pages):
		if counter < start_index: continue
		if counter > end_index: break
		print(f'============> {counter:05d} <============')

		# Прокликиваем все цвета товара и парсим страницу
		driver.get(url)

		try:
			colors_wrapper = driver.find_element_by_css_selector('.elementSkuPropertyList')
			color_nodes = colors_wrapper.find_elements_by_css_selector('.elementSkuPropertyValue')
			driver.execute_script("const a123 = document.querySelector('#footerLine'); if(a123) a123.style.display = 'none';")
		except Exception as e:
			print('NO .elementSkuPropertyList')
			colors_wrapper = None
			color_nodes = [False]
		
		if len(color_nodes) > 1:
			color_nodes[1].click()
			sleep(1)
			color_nodes[0].click()
			sleep(1)
		for node in color_nodes:
			inner_counter += 1
			target_filename = result_folder + f'{inner_counter:05d}' + '-' + result_file_path
			if node: node.click()
			sleep(1)
			parser = Client(url, target_filename)
			print(f'---> {inner_counter:05d} <---')
			print(url)
			parser.run()
			sleep(0.1)
