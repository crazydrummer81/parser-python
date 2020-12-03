# Практика использования selenuim

from selenium import webdriver
links = [
	'https://ru.zenithcrusher.com/products/beneficiation-equipment/sj-double-impeller-leaching-tank.html',
	'https://ru.zenithcrusher.com/products/beneficiation-equipment/desorption-and-electrolysis-unit.html'
]

chomedriver_path = 'chromedriver.exe'
driver = webdriver.Chrome(chomedriver_path)

for link in links:
	driver.get('https://ru.zenithcrusher.com/products/beneficiation-equipment/desorption-and-electrolysis-unit.html')
	# table = driver.find_elements_by_css_selector('table.para_table')
	table = driver.find_element_by_css_selector('table.para_table')
	print(table.get_attribute('outerHTML'))

driver.quit()