import os
import json
import os
from time import sleep
# from json2xml import json2xml
# from dicttoxml import dicttoxml
from datetime import datetime

def findItemByKey(obj, key):
	try:
		if key in obj: return obj[key]
		for k, v in obj.items():
			if isinstance(v,dict):
				item = findItemByKey(v, key)
				if item is not None:
						return item
	except:
		return False

now = datetime.now()
current_time = now.strftime("%y%m%d-%H%M%S")
print("Current Time =", current_time)

delimiter = '^'

source_folder = 'result-200907-092549/'
target_folder = 'csv/'
if not os.path.isdir(target_folder):
	os.mkdir(target_folder)
# target_filename = 'stanki-test' + '-' + current_time + '.csv'
# target_xml_filename = 'stanki-test' + '-' + current_time + '.xml'
target_filename = 'mechta-' + current_time + '.csv'
target_xml_filename = 'stanki-test.xml'
xml_id = 'MECHTAKZ'

files = os.listdir(source_folder)
limit = 10000
# os.remove(target_folder+target_filename)
# os.remove(target_folder+target_xml_filename)

ft = open(target_folder+target_filename, 'w+', encoding='utf-8')
# ftx = open(target_folder+target_xml_filename, 'w+', encoding='utf-8')

for i, filename in enumerate(files):
	if i >= limit: break
	if not os.path.isdir(source_folder+filename):
		print('-------> '+filename+' <-------')
		with open(source_folder+filename, 'r', encoding='utf-8') as fs:
			source_dict = json.load(fs)
			target_dict = {}
			try: 
				target_dict['IE_XML_ID'] =  xml_id + '' + f'{i+1:04d}' 
			except: # Внешний код (B_IBLOCK_ELEMENT.XML_ID) | 10 
				target_dict['IE_XML_ID'] = ''
			try: 
				target_dict['IE_NAME'] =  source_dict['product_name'] or '' 
			except:
				target_dict['IE_NAME'] = ''
			try: 
				target_dict['IE_ACTIVE'] =  'Y'
			except: # Активность (B_IBLOCK_ELEMENT.ACTIVE) | 40
				target_dict['IE_ACTIVE'] = ''
			try: 
				target_dict['IE_PREVIEW_PICTURE'] =  '' 
			except: # Картинка для анонса (B_IBLOCK_ELEMENT.PREVIEW_PICTURE) | 70
				target_dict['IE_PREVIEW_PICTURE'] = ''
			try: 
				target_dict['IE_PREVIEW_TEXT'] =  '' 
			except: # Описание для анонса (B_IBLOCK_ELEMENT.PREVIEW_TEXT) | 80 
				target_dict['IE_PREVIEW_TEXT'] = ''
			try: 
				target_dict['IE_PREVIEW_TEXT_TYPE'] =  '' 
			except: # Тип описания для анонса (B_IBLOCK_ELEMENT.PREVIEW_TEXT_TYPE) | 90 
				target_dict['IE_PREVIEW_TEXT_TYPE'] = ''
			try: 
				target_dict['IE_DETAIL_PICTURE'] =  source_dict['main_image']['url'] or '' 
			except:
				target_dict['IE_DETAIL_PICTURE'] = ''
			try: 
				target_dict['IE_DETAIL_TEXT'] =  source_dict['product_description']['content'] or '' 
			except:
				target_dict['IE_DETAIL_TEXT'] = ''
			try: 
				target_dict['IE_DETAIL_TEXT_TYPE'] =  'html'  
			except: # Тип детального описания (B_IBLOCK_ELEMENT.DETAIL_TEXT_TYPE) | 120 
				target_dict['IE_DETAIL_TEXT_TYPE'] = ''
			try: 
				target_dict['IE_CODE'] =  'html'  
			except: # Тип детального описания (B_IBLOCK_ELEMENT.DETAIL_TEXT_TYPE) | 120 
				target_dict['IE_CODE'] = ''
			try: 
				target_dict['IE_SORT'] =  'html'  
			except: # Тип детального описания (B_IBLOCK_ELEMENT.DETAIL_TEXT_TYPE) | 120 
				target_dict['IE_SORT'] = ''
			try: 
				target_dict['IE_TAGS'] =  'html'  
			except: # Тип детального описания (B_IBLOCK_ELEMENT.DETAIL_TEXT_TYPE) | 120 
				target_dict['IE_TAGS'] = ''
			try:	
				target_dict['IP_PROP2865'] =  source_dict['product_params']['SIM карта']['SIM-карта']
			except:
				target_dict['SIM-карта'] = ''
			try:	
				target_dict['IP_PROP2866'] =  source_dict['product_params']['Видеокарта']['Графический процессор']
			except:
				target_dict['Графический процессор'] = ''
			try:	
				target_dict['IP_PROP2867'] =  source_dict['product_params']['Звук']['Встроенные динамики']
			except:
				target_dict['Встроенные динамики'] = ''
			try:	
				target_dict['IP_PROP2868'] =  source_dict['product_params']['Звук']['Встроенный микрофон']
			except:
				target_dict['Встроенный микрофон'] = ''
			try:	
				target_dict['IP_PROP2869'] =  source_dict['product_params']['Звук']['Микрофон']
			except:
				target_dict['Микрофон'] = ''
			try:	
				target_dict['IP_PROP2870'] =  source_dict['product_params']['Интерфейсы']['HDMI']
			except:
				target_dict['HDMI'] = ''
			try:	
				target_dict['IP_PROP2871'] =  source_dict['product_params']['Интерфейсы']['Разъем для наушников']
			except:
				target_dict['Разъем для наушников'] = ''
			try:	
				target_dict['IP_PROP2872'] =  source_dict['product_params']['Информационные функции']['Индикация']
			except:
				target_dict['Индикация'] = ''
			try:	
				target_dict['IP_PROP2873'] =  source_dict['product_params']['Информационные функции']['Индикация уровня заряда']
			except:
				target_dict['Индикация уровня заряда'] = ''
			try:	
				target_dict['IP_PROP2874'] =  source_dict['product_params']['Комплектация']['Количество аккумуляторов в трубке']
			except:
				target_dict['Количество аккумуляторов в трубке'] = ''
			try:	
				target_dict['IP_PROP2875'] =  source_dict['product_params']['Комплектация']['Светочувствительность ISO']
			except:
				target_dict['Светочувствительность ISO'] = ''
			try:	
				target_dict['IP_PROP2876'] =  source_dict['product_params']['Корпус']['Количество трубок в комплекте']
			except:
				target_dict['Количество трубок в комплекте'] = ''
			try:	
				target_dict['IP_PROP2877'] =  source_dict['product_params']['Матрица']['Материал корпуса']
			except:
				target_dict['Материал корпуса'] = ''
			try:	
				target_dict['IP_PROP2878'] =  source_dict['product_params']['Матрица']['Тип и размер матрицы']
			except:
				target_dict['Тип и размер матрицы'] = ''
			try:	
				target_dict['IP_PROP2879'] =  source_dict['product_params']['Матрица']['Эффект. разрешение, Мпикс']
			except:
				target_dict['Эффект. разрешение, Мпикс'] = ''
			try:	
				target_dict['IP_PROP2880'] =  source_dict['product_params']['Операционная система']['Мобильная ОС']
			except:
				target_dict['Мобильная ОС'] = ''
			try:	
				target_dict['IP_PROP2881'] =  source_dict['product_params']['Оптика']['Объектив']
			except:
				target_dict['Объектив'] = ''
			try:	
				target_dict['IP_PROP2882'] =  source_dict['product_params']['Оптика']['Светосила (F-число)']
			except:
				target_dict['Светосила (F-число)'] = ''
			try:	
				target_dict['IP_PROP2883'] =  source_dict['product_params']['Оптика']['Фокусное расстояние']
			except:
				target_dict['Фокусное расстояние'] = ''
			try:	
				target_dict['IP_PROP2884'] =  source_dict['product_params']['Опции']['Дополнительные опции']
			except:
				target_dict['Дополнительные опции'] = ''
			try:	
				target_dict['IP_PROP2885'] =  source_dict['product_params']['Основные характеристики']['Ёмкость, мАч']
			except:
				target_dict['Ёмкость, мАч'] = ''
			try:	
				target_dict['IP_PROP2886'] =  source_dict['product_params']['Основные характеристики']['Автоответчик']
			except:
				target_dict['Автоответчик'] = ''
			try:	
				target_dict['IP_PROP2887'] =  source_dict['product_params']['Основные характеристики']['Возможность настенной установки']
			except:
				target_dict['Возможность настенной установки'] = ''
			try:	
				target_dict['IP_PROP2888'] =  source_dict['product_params']['Основные характеристики']['Дальность действия в помещении, м']
			except:
				target_dict['Дальность действия в помещении, м'] = ''
			try:	
				target_dict['IP_PROP2889'] =  source_dict['product_params']['Основные характеристики']['Диаметр мембран, мм']
			except:
				target_dict['Диаметр мембран, мм'] = ''
			try:	
				target_dict['IP_PROP2890'] =  source_dict['product_params']['Основные характеристики']['Диапазон воспроизводимых частот, Гц']
			except:
				target_dict['Диапазон воспроизводимых частот, Гц'] = ''
			try:	
				target_dict['IP_PROP2891'] =  source_dict['product_params']['Основные характеристики']['Диапазон частот, Гц']
			except:
				target_dict['Диапазон частот, Гц'] = ''
			try:	
				target_dict['IP_PROP2892'] =  source_dict['product_params']['Основные характеристики']['Дисплей']
			except:
				target_dict['Дисплей'] = ''
			try:	
				target_dict['IP_PROP2893'] =  source_dict['product_params']['Основные характеристики']['Дисплей трубки']
			except:
				target_dict['Дисплей трубки'] = ''
			try:	
				target_dict['IP_PROP2894'] =  source_dict['product_params']['Основные характеристики']['Длина кабеля, м']
			except:
				target_dict['Длина кабеля, м'] = ''
			try:	
				target_dict['IP_PROP2895'] =  source_dict['product_params']['Основные характеристики']['Для моделей']
			except:
				target_dict['Для моделей'] = ''
			try:	
				target_dict['IP_PROP2896'] =  source_dict['product_params']['Основные характеристики']['Для телефонов']
			except:
				target_dict['Для телефонов'] = ''
			try:	
				target_dict['IP_PROP2897'] =  source_dict['product_params']['Основные характеристики']['Защита от воды и пыли']
			except:
				target_dict['Защита от воды и пыли'] = ''
			try:	
				target_dict['IP_PROP2898'] =  source_dict['product_params']['Основные характеристики']['Индикатор уровня зарядки']
			except:
				target_dict['Индикатор уровня зарядки'] = ''
			try:	
				target_dict['IP_PROP2899'] =  source_dict['product_params']['Основные характеристики']['Количество каналов']
			except:
				target_dict['Количество каналов'] = ''
			try:	
				target_dict['IP_PROP2900'] =  source_dict['product_params']['Основные характеристики']['Количество раций в комплекте']
			except:
				target_dict['Количество раций в комплекте'] = ''
			try:	
				target_dict['IP_PROP2901'] =  source_dict['product_params']['Основные характеристики']['Количество сигналов вызова']
			except:
				target_dict['Количество сигналов вызова'] = ''
			try:	
				target_dict['IP_PROP2902'] =  source_dict['product_params']['Основные характеристики']['Макс. входное напряжение']
			except:
				target_dict['Макс. входное напряжение'] = ''
			try:	
				target_dict['IP_PROP2903'] =  source_dict['product_params']['Основные характеристики']['Максимальная высота, см']
			except:
				target_dict['Максимальная высота, см'] = ''
			try:	
				target_dict['IP_PROP2904'] =  source_dict['product_params']['Основные характеристики']['Максимальная нагрузка, кг']
			except:
				target_dict['Максимальная нагрузка, кг'] = ''
			try:	
				target_dict['IP_PROP2905'] =  source_dict['product_params']['Основные характеристики']['Максимальный вес нагрузки, кг']
			except:
				target_dict['Максимальный вес нагрузки, кг'] = ''
			try:	
				target_dict['IP_PROP2906'] =  source_dict['product_params']['Основные характеристики']['Материал сумки/чехла']
			except:
				target_dict['Материал сумки/чехла'] = ''
			try:	
				target_dict['IP_PROP2907'] =  source_dict['product_params']['Основные характеристики']['Минимальная высота, см']
			except:
				target_dict['Минимальная высота, см'] = ''
			try:	
				target_dict['IP_PROP2908'] =  source_dict['product_params']['Основные характеристики']['Мощность передатчика, Вт']
			except:
				target_dict['Мощность передатчика, Вт'] = ''
			try:	
				target_dict['IP_PROP2909'] =  source_dict['product_params']['Основные характеристики']['Наличие лицензии']
			except:
				target_dict['Наличие лицензии'] = ''
			try:	
				target_dict['IP_PROP2910'] =  source_dict['product_params']['Основные характеристики']['Определитель номера']
			except:
				target_dict['Определитель номера'] = ''
			try:	
				target_dict['IP_PROP2911'] =  source_dict['product_params']['Основные характеристики']['Память принятых вызовов']
			except:
				target_dict['Память принятых вызовов'] = ''
			try:	
				target_dict['IP_PROP2912'] =  source_dict['product_params']['Основные характеристики']['Повторный набор номера']
			except:
				target_dict['Повторный набор номера'] = ''
			try:	
				target_dict['IP_PROP2913'] =  source_dict['product_params']['Основные характеристики']['Рабочая частота, МГц']
			except:
				target_dict['Рабочая частота, МГц'] = ''
			try:	
				target_dict['IP_PROP2914'] =  source_dict['product_params']['Основные характеристики']['Рабочий диапазон температур, C']
			except:
				target_dict['Рабочий диапазон температур, C'] = ''
			try:	
				target_dict['IP_PROP2915'] =  source_dict['product_params']['Основные характеристики']['Радиус действия в помещении, м']
			except:
				target_dict['Радиус действия в помещении, м'] = ''
			try:	
				target_dict['IP_PROP2916'] =  source_dict['product_params']['Основные характеристики']['Радиус действия, км']
			except:
				target_dict['Радиус действия, км'] = ''
			try:	
				target_dict['IP_PROP2917'] =  source_dict['product_params']['Основные характеристики']['Радиус действия, м']
			except:
				target_dict['Радиус действия, м'] = ''
			try:	
				target_dict['IP_PROP2918'] =  source_dict['product_params']['Основные характеристики']['Размер ремешка, см']
			except:
				target_dict['Размер ремешка, см'] = ''
			try:	
				target_dict['IP_PROP2919'] =  source_dict['product_params']['Основные характеристики']['Режимы дисплея']
			except:
				target_dict['Режимы дисплея'] = ''
			try:	
				target_dict['IP_PROP2920'] =  source_dict['product_params']['Основные характеристики']['Ремешок']
			except:
				target_dict['Ремешок'] = ''
			try:	
				target_dict['IP_PROP2921'] =  source_dict['product_params']['Основные характеристики']['Совместимость']
			except:
				target_dict['Совместимость'] = ''
			try:	
				target_dict['IP_PROP2922'] =  source_dict['product_params']['Основные характеристики']['Совместимость со смартфономи']
			except:
				target_dict['Совместимость со смартфономи'] = ''
			try:	
				target_dict['IP_PROP2923'] =  source_dict['product_params']['Основные характеристики']['Спикерфон']
			except:
				target_dict['Спикерфон'] = ''
			try:	
				target_dict['IP_PROP2924'] =  source_dict['product_params']['Основные характеристики']['Текстовый дисплей трубки']
			except:
				target_dict['Текстовый дисплей трубки'] = ''
			try:	
				target_dict['IP_PROP2925'] =  source_dict['product_params']['Основные характеристики']['Телефонная книга']
			except:
				target_dict['Телефонная книга'] = ''
			try:	
				target_dict['IP_PROP2926'] =  source_dict['product_params']['Основные характеристики']['Тип кабеля (шнура)']
			except:
				target_dict['Тип кабеля (шнура)'] = ''
			try:	
				target_dict['IP_PROP2927'] =  source_dict['product_params']['Основные характеристики']['Тип наушников']
			except:
				target_dict['Тип наушников'] = ''
			try:	
				target_dict['IP_PROP2928'] =  source_dict['product_params']['Основные характеристики']['Тип подключения']
			except:
				target_dict['Тип подключения'] = ''
			try:	
				target_dict['IP_PROP2929'] =  source_dict['product_params']['Основные характеристики']['Тональный набор']
			except:
				target_dict['Тональный набор'] = ''
			try:	
				target_dict['IP_PROP2930'] =  source_dict['product_params']['Основные характеристики']['Управление']
			except:
				target_dict['Управление'] = ''
			try:	
				target_dict['IP_PROP2931'] =  source_dict['product_params']['Основные характеристики']['Управление через bluetooth']
			except:
				target_dict['Управление через bluetooth'] = ''
			try:	
				target_dict['IP_PROP2932'] =  source_dict['product_params']['Основные характеристики']['Управление через аудио линейный порт телефона']
			except:
				target_dict['Управление через аудио линейный порт телефона'] = ''
			try:	
				target_dict['IP_PROP2933'] =  source_dict['product_params']['Основные характеристики']['Формат записи']
			except:
				target_dict['Формат записи'] = ''
			try:	
				target_dict['IP_PROP2934'] =  source_dict['product_params']['Основные характеристики']['Число USB портов']
			except:
				target_dict['Число USB портов'] = ''
			try:	
				target_dict['IP_PROP2935'] =  source_dict['product_params']['Основные характеристики']['Чувствительность наушников, дБ/В']
			except:
				target_dict['Чувствительность наушников, дБ/В'] = ''
			try:	
				target_dict['IP_PROP2936'] =  source_dict['product_params']['Основные характеристики']['Чувствительность, дБ']
			except:
				target_dict['Чувствительность, дБ'] = ''
			try:	
				target_dict['IP_PROP2937'] =  source_dict['product_params']['Основные характеристики']['Штекер']
			except:
				target_dict['Штекер'] = ''
			try:	
				target_dict['IP_PROP2938'] =  source_dict['product_params']['Основные характеристики']['я удален']
			except:
				target_dict['я удален'] = ''
			try:	
				target_dict['IP_PROP2939'] =  source_dict['product_params']['Память']['Встроенная память, Гб']
			except:
				target_dict['Встроенная память, Гб'] = ''
			try:	
				target_dict['IP_PROP2940'] =  source_dict['product_params']['Память']['Максимальная емкость карты памяти, Гб']
			except:
				target_dict['Максимальная емкость карты памяти, Гб'] = ''
			try:	
				target_dict['IP_PROP2941'] =  source_dict['product_params']['Память']['Объем оперативной памяти, Гб']
			except:
				target_dict['Объем оперативной памяти, Гб'] = ''
			try:	
				target_dict['IP_PROP2942'] =  source_dict['product_params']['Память']['Объем памяти, ГБ']
			except:
				target_dict['Объем памяти, ГБ'] = ''
			try:	
				target_dict['IP_PROP2943'] =  source_dict['product_params']['Память']['Тип карты памяти']
			except:
				target_dict['Тип карты памяти'] = ''
			try:	
				target_dict['IP_PROP2944'] =  source_dict['product_params']['Память']['Тип носителя данных']
			except:
				target_dict['Тип носителя данных'] = ''
			try:	
				target_dict['IP_PROP2945'] =  source_dict['product_params']['Питание']['Беспроводная зарядка']
			except:
				target_dict['Беспроводная зарядка'] = ''
			try:	
				target_dict['IP_PROP2946'] =  source_dict['product_params']['Питание']['Быстрая зарядка']
			except:
				target_dict['Быстрая зарядка'] = ''
			try:	
				target_dict['IP_PROP2947'] =  source_dict['product_params']['Питание']['Время в режиме ожидания, ч']
			except:
				target_dict['Время в режиме ожидания, ч'] = ''
			try:	
				target_dict['IP_PROP2948'] =  source_dict['product_params']['Питание']['Время в режиме разговора, ч']
			except:
				target_dict['Время в режиме разговора, ч'] = ''
			try:	
				target_dict['IP_PROP2949'] =  source_dict['product_params']['Питание']['Время зарядки']
			except:
				target_dict['Время зарядки'] = ''
			try:	
				target_dict['IP_PROP2950'] =  source_dict['product_params']['Питание']['Время зарядки аккумулятора, ч']
			except:
				target_dict['Время зарядки аккумулятора, ч'] = ''
			try:	
				target_dict['IP_PROP2951'] =  source_dict['product_params']['Питание']['Время работы от аккумулятора, ч']
			except:
				target_dict['Время работы от аккумулятора, ч'] = ''
			try:	
				target_dict['IP_PROP2952'] =  source_dict['product_params']['Питание']['Емкость аккумулятора, мАч']
			except:
				target_dict['Емкость аккумулятора, мАч'] = ''
			try:	
				target_dict['IP_PROP2953'] =  source_dict['product_params']['Питание']['Питание']
			except:
				target_dict['Питание'] = ''
			try:	
				target_dict['IP_PROP2954'] =  source_dict['product_params']['Питание']['Работа от аккумулятора, ч']
			except:
				target_dict['Работа от аккумулятора, ч'] = ''
			try:	
				target_dict['IP_PROP2955'] =  source_dict['product_params']['Питание']['Размер аккумулятора']
			except:
				target_dict['Размер аккумулятора'] = ''
			try:	
				target_dict['IP_PROP2956'] =  source_dict['product_params']['Питание']['Тип аккумулятора']
			except:
				target_dict['Тип аккумулятора'] = ''
			try:	
				target_dict['IP_PROP2957'] =  source_dict['product_params']['Процессор']['Модель процессора']
			except:
				target_dict['Модель процессора'] = ''
			try:	
				target_dict['IP_PROP2958'] =  source_dict['product_params']['Процессор']['Процессор, (МГц, количество ядер)']
			except:
				target_dict['Процессор, (МГц, количество ядер)'] = ''
			try:	
				target_dict['IP_PROP2959'] =  source_dict['product_params']['Разное']['LBS']
			except:
				target_dict['LBS'] = ''
			try:	
				target_dict['IP_PROP2960'] =  source_dict['product_params']['Разное']['Гарантия']
			except:
				target_dict['Гарантия'] = ''
			try:	
				target_dict['IP_PROP2961'] =  source_dict['product_params']['Разное']['Длина кабеля']
			except:
				target_dict['Длина кабеля'] = ''
			try:	
				target_dict['IP_PROP2962'] =  source_dict['product_params']['Разное']['Для корпуса размером, мм']
			except:
				target_dict['Для корпуса размером, мм'] = ''
			try:	
				target_dict['IP_PROP2963'] =  source_dict['product_params']['Разное']['Дополнительно']
			except:
				target_dict['Дополнительно'] = ''
			try:	
				target_dict['IP_PROP2964'] =  source_dict['product_params']['Разное']['Индикатор состояния']
			except:
				target_dict['Индикатор состояния'] = ''
			try:	
				target_dict['IP_PROP2965'] =  source_dict['product_params']['Разное']['Кнопки управления']
			except:
				target_dict['Кнопки управления'] = ''
			try:	
				target_dict['IP_PROP2966'] =  source_dict['product_params']['Разное']['Компас']
			except:
				target_dict['Компас'] = ''
			try:	
				target_dict['IP_PROP2967'] =  source_dict['product_params']['Разное']['Комплектация']
			except:
				target_dict['Комплектация'] = ''
			try:	
				target_dict['IP_PROP2968'] =  source_dict['product_params']['Разное']['Крепление на ремень']
			except:
				target_dict['Крепление на ремень'] = ''
			try:	
				target_dict['IP_PROP2969'] =  source_dict['product_params']['Разное']['Макс. выходное напряжение']
			except:
				target_dict['Макс. выходное напряжение'] = ''
			try:	
				target_dict['IP_PROP2970'] =  source_dict['product_params']['Разное']['Материал']
			except:
				target_dict['Материал'] = ''
			try:	
				target_dict['IP_PROP2971'] =  source_dict['product_params']['Разное']['Материал ремешка']
			except:
				target_dict['Материал ремешка'] = ''
			try:	
				target_dict['IP_PROP2972'] =  source_dict['product_params']['Разное']['Модель']
			except:
				target_dict['Модель'] = ''
			try:	
				target_dict['IP_PROP2973'] =  source_dict['product_params']['Разное']['Наличие регулятора громкости']
			except:
				target_dict['Наличие регулятора громкости'] = ''
			try:	
				target_dict['IP_PROP2974'] =  source_dict['product_params']['Разное']['Поддержка 5G']
			except:
				target_dict['Поддержка 5G'] = ''
			try:	
				target_dict['IP_PROP2975'] =  source_dict['product_params']['Разное']['Поддержка видеозвонков']
			except:
				target_dict['Поддержка видеозвонков'] = ''
			try:	
				target_dict['IP_PROP2976'] =  source_dict['product_params']['Разное']['Поддержка голосовой связи']
			except:
				target_dict['Поддержка голосовой связи'] = ''
			try:	
				target_dict['IP_PROP2977'] =  source_dict['product_params']['Разное']['Поддержка казахского языка']
			except:
				target_dict['Поддержка казахского языка'] = ''
			try:	
				target_dict['IP_PROP2978'] =  source_dict['product_params']['Разное']['Поддержка сервисов Google Play']
			except:
				target_dict['Поддержка сервисов Google Play'] = ''
			try:	
				target_dict['IP_PROP2979'] =  source_dict['product_params']['Разное']['Подключение дополнительных трубок']
			except:
				target_dict['Подключение дополнительных трубок'] = ''
			try:	
				target_dict['IP_PROP2980'] =  source_dict['product_params']['Разное']['Процессор']
			except:
				target_dict['Процессор'] = ''
			try:	
				target_dict['IP_PROP2981'] =  source_dict['product_params']['Разное']['Серия']
			except:
				target_dict['Серия'] = ''
			try:	
				target_dict['IP_PROP2982'] =  source_dict['product_params']['Разное']['Страна производитель']
			except:
				target_dict['Страна производитель'] = ''
			try:	
				target_dict['IP_PROP2983'] =  source_dict['product_params']['Разное']['Тип батареи']
			except:
				target_dict['Тип батареи'] = ''
			try:	
				target_dict['IP_PROP2984'] =  source_dict['product_params']['Разное']['Фонарик']
			except:
				target_dict['Фонарик'] = ''
			try:	
				target_dict['IP_PROP2985'] =  source_dict['product_params']['Разное']['Фотокамера']
			except:
				target_dict['Фотокамера'] = ''
			try:	
				target_dict['IP_PROP2986'] =  source_dict['product_params']['Разное']['Шумоподавление']
			except:
				target_dict['Шумоподавление'] = ''
			try:	
				target_dict['IP_PROP2987'] =  source_dict['product_params']['Разное']['Стандарты сети']
			except:
				target_dict['Стандарты сети'] = ''
			try:	
				target_dict['IP_PROP2988'] =  source_dict['product_params']['Разное']['Формат мелодии']
			except:
				target_dict['Формат мелодии'] = ''
			try:	
				target_dict['IP_PROP2989'] =  source_dict['product_params']['Стандарт']['ANT+']
			except:
				target_dict['ANT+'] = ''
			try:	
				target_dict['IP_PROP2990'] =  source_dict['product_params']['Типы передачи данных']['Bluetooth']
			except:
				target_dict['Bluetooth'] = ''
			try:	
				target_dict['IP_PROP2991'] =  source_dict['product_params']['Типы передачи данных']['GPRS']
			except:
				target_dict['GPRS'] = ''
			try:	
				target_dict['IP_PROP2992'] =  source_dict['product_params']['Типы передачи данных']['GPS']
			except:
				target_dict['GPS'] = ''
			try:	
				target_dict['IP_PROP2993'] =  source_dict['product_params']['Типы передачи данных']['NFC']
			except:
				target_dict['NFC'] = ''
			try:	
				target_dict['IP_PROP2994'] =  source_dict['product_params']['Типы передачи данных']['USB']
			except:
				target_dict['USB'] = ''
			try:	
				target_dict['IP_PROP2995'] =  source_dict['product_params']['Типы передачи данных']['WAP']
			except:
				target_dict['WAP'] = ''
			try:	
				target_dict['IP_PROP2996'] =  source_dict['product_params']['Типы передачи данных']['Wi-Fi']
			except:
				target_dict['Wi-Fi'] = ''
			try:	
				target_dict['IP_PROP2997'] =  source_dict['product_params']['Типы передачи данных']['Поддержка 4G (LTE)']
			except:
				target_dict['Поддержка 4G (LTE)'] = ''
			try:	
				target_dict['IP_PROP2998'] =  source_dict['product_params']['Фотокамера']['Автофокус']
			except:
				target_dict['Автофокус'] = ''
			try:	
				target_dict['IP_PROP2999'] =  source_dict['product_params']['Фотокамера']['Макс. разрешение фотоснимков, Пикс']
			except:
				target_dict['Макс. разрешение фотоснимков, Пикс'] = ''
			try:	
				target_dict['IP_PROP3000'] =  source_dict['product_params']['Фотокамера']['Особенности тыловой камеры']
			except:
				target_dict['Особенности тыловой камеры'] = ''
			try:	
				target_dict['IP_PROP3001'] =  source_dict['product_params']['Фотокамера']['Особенности фронтальной камеры']
			except:
				target_dict['Особенности фронтальной камеры'] = ''
			try:	
				target_dict['IP_PROP3002'] =  source_dict['product_params']['Фотокамера']['Разрешение фотокамеры, Мпикс']
			except:
				target_dict['Разрешение фотокамеры, Мпикс'] = ''
			try:	
				target_dict['IP_PROP3003'] =  source_dict['product_params']['Фотокамера']['Режим видеосъемки']
			except:
				target_dict['Режим видеосъемки'] = ''
			try:	
				target_dict['IP_PROP3004'] =  source_dict['product_params']['Фотокамера']['Фронтальная камера (для видеозвонков), Мпикс']
			except:
				target_dict['Фронтальная камера (для видеозвонков), Мпикс'] = ''
			try:	
				target_dict['IP_PROP3005'] =  source_dict['product_params']['Функции']['Сканер отпечатка пальца']
			except:
				target_dict['Сканер отпечатка пальца'] = ''
			try:	
				target_dict['IP_PROP3006'] =  source_dict['product_params']['Функции']['Акселерометр']
			except:
				target_dict['Акселерометр'] = ''
			try:	
				target_dict['IP_PROP3007'] =  source_dict['product_params']['Функции']['Барометр']
			except:
				target_dict['Барометр'] = ''
			try:	
				target_dict['IP_PROP3008'] =  source_dict['product_params']['Функции']['Блокировка клавиатуры']
			except:
				target_dict['Блокировка клавиатуры'] = ''
			try:	
				target_dict['IP_PROP3009'] =  source_dict['product_params']['Функции']['Вибрация']
			except:
				target_dict['Вибрация'] = ''
			try:	
				target_dict['IP_PROP3010'] =  source_dict['product_params']['Функции']['Встроенное оборудование и функции']
			except:
				target_dict['Встроенное оборудование и функции'] = ''
			try:	
				target_dict['IP_PROP3011'] =  source_dict['product_params']['Функции']['Гироскоп']
			except:
				target_dict['Гироскоп'] = ''
			try:	
				target_dict['IP_PROP3012'] =  source_dict['product_params']['Функции']['Голосовой набор']
			except:
				target_dict['Голосовой набор'] = ''
			try:	
				target_dict['IP_PROP3013'] =  source_dict['product_params']['Функции']['Датчик освещенности']
			except:
				target_dict['Датчик освещенности'] = ''
			try:	
				target_dict['IP_PROP3014'] =  source_dict['product_params']['Функции']['Датчик сердечного ритма']
			except:
				target_dict['Датчик сердечного ритма'] = ''
			try:	
				target_dict['IP_PROP3015'] =  source_dict['product_params']['Функции']['Ожидание/удержание вызова']
			except:
				target_dict['Ожидание/удержание вызова'] = ''
			try:	
				target_dict['IP_PROP3016'] =  source_dict['product_params']['Функции']['Ответить/закончить разговор']
			except:
				target_dict['Ответить/закончить разговор'] = ''
			try:	
				target_dict['IP_PROP3017'] =  source_dict['product_params']['Функции']['Панорамная съемка']
			except:
				target_dict['Панорамная съемка'] = ''
			try:	
				target_dict['IP_PROP3018'] =  source_dict['product_params']['Функции']['Повтор последнего номера']
			except:
				target_dict['Повтор последнего номера'] = ''
			try:	
				target_dict['IP_PROP3019'] =  source_dict['product_params']['Функции']['Подтверждение окончания передачи']
			except:
				target_dict['Подтверждение окончания передачи'] = ''
			try:	
				target_dict['IP_PROP3020'] =  source_dict['product_params']['Функции']['Распознавание лица']
			except:
				target_dict['Распознавание лица'] = ''
			try:	
				target_dict['IP_PROP3021'] =  source_dict['product_params']['Функции']['Режим мониторинга/сканирования']
			except:
				target_dict['Режим мониторинга/сканирования'] = ''
			try:	
				target_dict['IP_PROP3022'] =  source_dict['product_params']['Функции']['Режимы видеосъемки']
			except:
				target_dict['Режимы видеосъемки'] = ''
			try:	
				target_dict['IP_PROP3023'] =  source_dict['product_params']['Функции']['Система стабилизации изображения']
			except:
				target_dict['Система стабилизации изображения'] = ''
			try:	
				target_dict['IP_PROP3024'] =  source_dict['product_params']['Цвет, размеры и вес']['Вес без упаковки (нетто), кг']
			except:
				target_dict['Вес без упаковки (нетто), кг'] = ''
			try:	
				target_dict['IP_PROP3025'] =  source_dict['product_params']['Цвет, размеры и вес']['Вес в упаковке (брутто), кг']
			except:
				target_dict['Вес в упаковке (брутто), кг'] = ''
			try:	
				target_dict['IP_PROP3026'] =  source_dict['product_params']['Цвет, размеры и вес']['Вес трубки, гр']
			except:
				target_dict['Вес трубки, гр'] = ''
			try:	
				target_dict['IP_PROP3027'] =  source_dict['product_params']['Цвет, размеры и вес']['Габариты в упаковке (ВхШхГ), см']
			except:
				target_dict['Габариты в упаковке (ВхШхГ), см'] = ''
			try:	
				target_dict['IP_PROP3028'] =  source_dict['product_params']['Цвет, размеры и вес']['Габариты устройства (ВхШхГ), см']
			except:
				target_dict['Габариты устройства (ВхШхГ), см'] = ''
			try:	
				target_dict['IP_PROP3029'] =  source_dict['product_params']['Цвет, размеры и вес']['Размер базы (ВхШхГ), мм']
			except:
				target_dict['Размер базы (ВхШхГ), мм'] = ''
			try:	
				target_dict['IP_PROP3030'] =  source_dict['product_params']['Цвет, размеры и вес']['Размер трубки (ВхШхГ), мм']
			except:
				target_dict['Размер трубки (ВхШхГ), мм'] = ''
			try:	
				target_dict['IP_PROP3031'] =  source_dict['product_params']['Цвет, размеры и вес']['Цвет']
			except:
				target_dict['Цвет'] = ''
			try:	
				target_dict['IP_PROP3032'] =  source_dict['product_params']['Экран']['Датчик ориентации экрана']
			except:
				target_dict['Датчик ориентации экрана'] = ''
			try:	
				target_dict['IP_PROP3033'] =  source_dict['product_params']['Экран']['Диагональ экрана, дюйм']
			except:
				target_dict['Диагональ экрана, дюйм'] = ''
			try:	
				target_dict['IP_PROP3034'] =  source_dict['product_params']['Экран']['Количество цветов дисплея']
			except:
				target_dict['Количество цветов дисплея'] = ''
			try:	
				target_dict['IP_PROP3035'] =  source_dict['product_params']['Экран']['Контраст']
			except:
				target_dict['Контраст'] = ''
			try:	
				target_dict['IP_PROP3036'] =  source_dict['product_params']['Экран']['Разрешение']
			except:
				target_dict['Разрешение'] = ''
			try:	
				target_dict['IP_PROP3037'] =  source_dict['product_params']['Экран']['Разрешение дисплея, пикс']
			except:
				target_dict['Разрешение дисплея, пикс'] = ''
			try:	
				target_dict['IP_PROP3038'] =  source_dict['product_params']['Экран']['Сенсорный дисплей']
			except:
				target_dict['Сенсорный дисплей'] = ''
			try:	
				target_dict['IP_PROP3039'] =  source_dict['product_params']['Экран']['Технология изготовления дисплея']
			except:
				target_dict['Технология изготовления дисплея'] = ''
			try:	
				target_dict['IP_PROP3040'] =  source_dict['product_params']['Экран']['Формат']
			except:
				target_dict['Формат'] = ''
			try:	
				target_dict['IP_PROP3041'] =  source_dict['product_params']['Экран']['Частота обновления, Гц']
			except:
				target_dict['Частота обновления, Гц'] = ''
			try: 
				target_dict['IC_GROUP0'] =  source_dict['product_category_chain'][0] # Группа уровня (1) | 2150 
			except:
				target_dict['IC_GROUP0'] = ''
			try: 
				target_dict['IC_GROUP1'] =  source_dict['product_category_chain'][1] # Группа уровня (2) | 2160 
			except:
				target_dict['IC_GROUP1'] = ''
			try: 
				target_dict['IC_GROUP2'] =  source_dict['product_category_chain'][2] # Группа уровня (3) | 2170 
			except:
				target_dict['IC_GROUP2'] = ''
			try: 
				target_dict['IC_GROUP3'] =  source_dict['product_category_chain'][3] # Группа уровня (3) | 2170 
			except:
				target_dict['IC_GROUP3'] = ''
			try: 
				target_dict['IC_GROUP4'] =  source_dict['product_category_chain'][4] # Группа уровня (3) | 2170 
			except:
				target_dict['IC_GROUP4'] = ''
			try: 
				target_dict['IMAGES'] =  '$'.join([item['url'] for item in source_dict['additional_images']]) or '' 
			except:
				target_dict['IMAGES'] = ''
			try: 
				# print(source_dict['product_price']['full'])
				target_dict['PRICE'] = str(source_dict['product_price']['full'])
			except:
				target_dict['PRICE'] = ''

			target_dict['PRICE_CURRENCY'] = 'KZT'
			target_dict['QUANTITY'] = '10'


			csv_line_list = list(value for value in target_dict.values())
			first_line = delimiter.join(target_dict.keys()) if i == 0 else '' # print(csv_line_list)
			csv_line = first_line + '\n' + delimiter.join(csv_line_list)
			ft.write(csv_line)
			# ftx.write(dicttoxml(source_dict))
			# ftx.write(str(dicttoxml(source_dict)))
ft.close()
# ftx.close()