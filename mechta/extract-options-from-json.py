import os
import json

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%y%m%d-%H%M%S")

propertiesGroups = set()
properties = set()
propertiesWithValues = set()

source_folder = 'result/'
target_folder = 'options/'
if not os.path.isdir(target_folder):
	os.mkdir(target_folder)
target_filename_0 = current_time + '-groups-' + '.txt'
target_filename_1 = current_time + '-groups-properties-' + '.txt'
target_filename_2 = current_time + '-groups-properties-values-' + '.txt'
files = os.listdir(source_folder)

limit = 5000
ft0 = open(target_folder+target_filename_0, 'w', encoding='utf-8')
ft1 = open(target_folder+target_filename_1, 'w', encoding='utf-8')
ft2 = open(target_folder+target_filename_2, 'w', encoding='utf-8')
for i, filename in enumerate(files):
	if i > limit: break
	if not os.path.isdir(source_folder+filename):
		with open(source_folder+filename, 'r', encoding='utf-8') as fs:
			product = json.loads(fs.read())
			print(filename)
			
			# Формирование результата по продукту
			prodProps = product['product_params']
			groupStr = ''
			for group in prodProps:
				count = 0
				for prop in prodProps[group]:
					count += 1
					if count > 7: print('-'*50 + '> ' + filename)
					propertiesGroups.add(group.strip())
					properties.add(' ^ '.join([group.strip(), prop.strip()]))
					propertiesWithValues.add(' ^ '.join([group.strip(), prop.strip(), prodProps[group][prop].strip()]))

# Запись результата в файл
ft0.write('\n'.join(sorted(propertiesGroups)))
ft1.write('\n'.join(sorted(properties)))
ft2.write('\n'.join(sorted(propertiesWithValues)))
ft0.close()
ft1.close()
ft2.close()
