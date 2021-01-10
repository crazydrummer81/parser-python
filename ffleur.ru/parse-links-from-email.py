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
from time import sleep

import requests
import bs4
from selenium import webdriver
# chomedriver_path = 'D:\Distr\Coding\Parsing\geckodriver.exe'
firefox_profile = webdriver.FirefoxProfile()
# firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
# To prevent download dialog
firefox_profile.set_preference('browser.download.folderList', 2) # custom location
firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
firefox_profile.set_preference('browser.download.dir', '/tmp')
firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
driver = webdriver.Firefox(firefox_profile=firefox_profile)
# driver = webdriver.Firefox()

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

#! Переходим по страница почты, кликаем и достаем ссылки, загоняем в массив
base_link = 'https://mail.rambler.ru/folder/DG-3D/DG-3D-'
page_get = ''
start_page = 1
end_page = 98
#todo запустить браузер, запросить подтверждение входа в аккаунт
driver.get('https://rambler.ru')
print('Войди в аккаунт rutube и нажми здесь ENTER...')
input()
result_links = []
for page in range(start_page, end_page+1):
	# проходим по всем страницам
	url_param = '' if page == 0 else page_get + str(page)
	url = base_link + url_param
	print(url)
	driver.get(url)
	sleep(4)
	all_links = driver.find_elements_by_css_selector('a')
	for link in all_links:
		href = link.get_attribute('href')
		if '3d-download.php' in href:
			# КАЧАЕМ!!!
			link.click()
			sleep(2)
