import os
import json
import os
from time import sleep
# from json2xml import json2xml
# from dicttoxml import dicttoxml
from datetime import datetime
import re

now = datetime.now()
current_time = now.strftime("%y%m%d-%H%M%S")
print("Current Time =", current_time)

csv_headers = ['IE_XML_ID', 'IE_NAME', 'IE_ID', 'IE_ACTIVE', 'IE_ACTIVE_FROM', 'IE_ACTIVE_TO', 'IE_PREVIEW_PICTURE', 'IE_PREVIEW_TEXT', 'IE_PREVIEW_TEXT_TYPE', 'IE_DETAIL_PICTURE', 'IE_DETAIL_TEXT', 'IE_DETAIL_TEXT_TYPE', 'IE_CODE', 'IE_SORT', 'IE_TAGS', 'IP_PROP927', 'IP_PROP926', 'IC_GROUP0', 'IC_GROUP1', 'IC_GROUP2']

csv_line = {
	"IE_XML_ID" : '',
	"IE_NAME" : '',
	"IE_ID" : '',
	"IE_ACTIVE" : '',
	"IE_ACTIVE_FROM" : '',
	"IE_ACTIVE_TO" : '',
	"IE_PREVIEW_PICTURE" : '',
	"IE_PREVIEW_TEXT" : '',
	"IE_PREVIEW_TEXT_TYPE" : '',
	"IE_DETAIL_PICTURE" : '',
	"IE_DETAIL_TEXT" : '',
	"IE_DETAIL_TEXT_TYPE" : '',
	"IE_CODE" : '',
	"IE_SORT" : '',
	"IE_TAGS" : '',
	"IP_PROP927" : '',
	"IP_PROP926" : '',
	"IC_GROUP0" : '',
	"IC_GROUP1" : '',
	"IC_GROUP2" : ''
}
csv_headers = csv_line.keys()
delimiter = '^'

source_folder = 'result-200910-100000/'
result_folder = 'csv/'
if not os.path.isdir(result_folder):
	os.mkdir(result_folder)
# target_filename = 'stanki-test' + '-' + current_time + '.csv'
# target_xml_filename = 'stanki-test' + '-' + current_time + '.xml'
target_filename = 'zenithcrusher-' + current_time + '.csv'
xml_id = 'ZENITHCRUSHER'

files = os.listdir(source_folder)
resutl_csv = delimiter.join(csv_headers) + '\n'
limit = 10000
# os.remove(result_folder+target_filename)
# os.remove(result_folder+target_xml_filename)

ft = open(result_folder+target_filename, 'w+', encoding='utf-8')
# ftx = open(result_folder+target_xml_filename, 'w+', encoding='utf-8')

ft.write(delimiter.join(csv_headers) + '\n')
for i, filename in enumerate(files):
	if i >= limit: break
	if not os.path.isdir(source_folder+filename):
		print('-------> '+filename+' <-------')
		with open(source_folder+filename, 'r', encoding='utf-8') as fs:
			source_dict = json.load(fs)

			target_dict = {
				"IE_XML_ID" : xml_id + f'{i+1:04d}',
				"IE_NAME" : source_dict['product_name'],
				"IE_ID" : '',
				"IE_ACTIVE" : '',
				"IE_ACTIVE_FROM" : '',
				"IE_ACTIVE_TO" : '',
				"IE_PREVIEW_PICTURE" : source_dict['pruduct_detail_image'),
				"IE_PREVIEW_TEXT" : source_dict['product_preview_text'],
				"IE_PREVIEW_TEXT_TYPE" : 'html',
				"IE_DETAIL_PICTURE" : source_dict['pruduct_detail_image'],
				"IE_DETAIL_TEXT" : (
					'<div class="product_info"><div class="product_info__description">'
						+ source_dict['product_detail_text']
					+'</div>'
					+'<div class="product_info__characteristics"><table>'
						+ source_dict['product_characteristics_html']
					+'</table></div></div>'
						)
						.replace('https://hangcha.com.ru/wp-content/uploads/2020', 'pogruzchiki')
						.replace('"', '""'),
				"IE_DETAIL_TEXT_TYPE" : 'html',
				"IE_CODE" : '',
				"IE_SORT" : '500',
				"IE_TAGS" : '',
				"IP_PROP927" : 'Hangcha',
				"IP_PROP926" : 'Китай',
				"IC_GROUP0" : source_dict['product_category']['parent_name'],
				"IC_GROUP1" : source_dict['product_category']['name'],
				"IC_GROUP2" : '',
			}
			csv_line_list = list(value for value in target_dict.values())
			csv_line = delimiter.join(csv_line_list)
			ft.write(csv_line + '\n')
			# ftx.write(dicttoxml(source_dict))
			# ftx.write(str(dicttoxml(source_dict)))
ft.close()
# ftx.close()