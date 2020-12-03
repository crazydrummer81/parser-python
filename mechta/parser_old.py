import logging
import collections
import re
import csv
import json
import time
import cssutils

import requests
import bs4


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')



HEADERS = (
    'source_url',
    'product_category',
    'product_name',
    'manufacturer',
    'country',
    'main_image',
    'additional_images_urls',
    'product_params',
    'product_description',
    'product_description_images',
)


class Client:

    ParseResult = {
        'source_url': '',
        'product_category': '',
        'product_name': '',
        'manufacturer': '',
        'country': '',
        'main_image': '',
        'additional_images_urls': '',
        'product_params': '',
        'product_description': '',
        'product_description_images': '',
    }

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

        container = soup.select('div.breadcrumbs')
        for block in container:
            self.parse_category(block=block)

        container = soup.select('div.aa_catalogdetail')
        for block in container:
            self.parse_main_block(block=block)

        container = soup.select('div.productTabs')
        for block in container:
            self.parse_details_block(block=block)

        # Парсим H1
        container = soup.select('h1.iwr')
        for block in container:
            self.parse_details_block(block=block)
    
    def parse_h1(self, block):
        # Product name ----------------------------------------
        # product_name_block = block.select_one('h1.productMain__name')
        try:
            product_name = '"%s"' % block.get_text()
        except:
            product_name = '"%s"' % ''

        if not product_name:
            logger.debug('no product name')
            # return
        self.ParseResult['product_name'] = product_name


    def parse_category(self, block):
        product_categories_tree = block.select('div.bx-breadcrumb-item')

        last_item = None
        last_item = product_categories_tree[len(product_categories_tree)-1] if product_categories_tree[len(product_categories_tree)-1] else ''
        parent_item = product_categories_tree[len(product_categories_tree)-2] if product_categories_tree[len(product_categories_tree)-2] else ''
        for last_item in product_categories_tree:pass
        # if last_item:
        try:
            product_category = '{ "name": "%s", "url": "%s", "parent": "%s", "parent_url": "%s" }' % ( last_item.get_text(), last_item.select_one('a').get('href'), parent_item.get_text(), parent_item.select_one('a').get('href') )
        except:
            product_category = '{ "name": "%s", "url": "%s", "parent": "%s", "parent_url": "%s" }' % ( '','','','' )

        # else:
        #     product_category = ''

        logger.debug('\n%s', product_category)

        self.ParseResult['product_category'] = product_category

    def parse_main_block(self, block):
        # logger.debug(block)
        # print('=' * 100)

        # Main image-------------------------------------------
        image_block = block.select_one('a.aa_e_img')
        if not image_block:
            logger.error('not url block')
            # return

        a_style = image_block['style']
        style = cssutils.parseStyle(a_style)
        main_image_url = style['background-image']
        main_image_url = main_image_url.replace('url(', '').replace(')', '')

        # main_image_url = image_block.get('href')
        if not main_image_url:
            logger.error('no href')
            # return

        main_image_img = image_block.select_one('img')
        if (main_image_img):
            try:
                main_image = '{ "url": "%s", "alt": "%s" }' % ( main_image_url, main_image_img.get('alt') )
            except:
                main_image = '{ "url": "%s", "alt": "%s" }' % ( '', '' )

        # Additional images -----------------------------------
        additional_images_block = block.select_one('div.ok_e_nav_bl')
        additional_images_items = additional_images_block.select('img')
        additional_images_urls = '[ ';
        for item in additional_images_items:
            # item_alt = item.select_one('img')
            try:
                additional_images_urls += '{ "url": "%s", "alt": "%s" }, ' % ( item.get('href'), item.get('alt') )
            except:
                additional_images_urls += '{ "url": "%s", "alt": "%s" }, ' % ( '','' )
        # urls = additional_images_items.get('href')
        additional_images_urls = re.sub(r',\s$', '', additional_images_urls) + ' ]'
        if not additional_images_block:
            logger.debug('no additional images')
            # return

        # Product name ----------------------------------------
        # product_name_block = block.select_one('h1.productMain__name')
        # try:
        #     product_name = '"%s"' % product_name_block.get_text()
        # except:
        #     product_name = '"%s"' % ''

        # if not product_name:
        #     logger.debug('no product name')
            # return

        # Product params -----------------------------------
        product_params_blocks = block.select('div.aa_dt_p1')
        for params_column in product_params_blocks:
            for param_line in params_column:
                if param_line.div.class['aa_dtprop_h'] 


        product_params = product_params_block.decode_contents()
        product_params = re.sub(r'\s+', ' ', product_params)
        product_params = '"%s"' % re.sub(r'"', '\\"', product_params)
        product_params_items = product_params_block.select('p')
        product_params = '{ '
        for item in product_params_items:
            param = item.get_text().split(':');
            product_params += '"%s": "%s", ' % (param[0].strip(), param[1].strip())
        product_params = re.sub(r',\s$', '', product_params)
        product_params += '}'
        if not product_params:
            logger.debug('no params')
            # return

        # Manufacturer Brand ------------------------------------
        product_manufacturer_block = block.select_one('a.productMain__manufacturer')
        try:
            manufacturer = '"%s"' % product_manufacturer_block.select_one('img').get('alt')
        except:
            manufacturer = '""'
        if not manufacturer:
            logger.debug('no manufactutrer')
            # return

        # Counrty ------------------------------------------------
        product_country_block = block.select_one('.productMain__country')
        try:
            country = '"%s"' % product_country_block.select_one('img').get('alt')
        except:
            country = '""'
        if not country:
            logger.debug('no manufactutrer')
            # return

        logger.debug('\n%s\n%s\n%s\n%s\n%s\n%s', product_name, manufacturer, country, main_image, additional_images_urls, product_params)

        # self.ParseResult['product_name'] = product_name
        self.ParseResult['manufacturer'] = manufacturer
        self.ParseResult['country'] = country
        self.ParseResult['main_image'] = main_image
        self.ParseResult['additional_images_urls'] = additional_images_urls
        # self.ParseResult['product_params'] = product_params

    # Params full -----------------------------------
    def parse_details_block(self, block):

        # Product characteristics ----------------------------
        # product_characteristics_block = block.select_one('.productTabs__item_characteristics')
        # product_characteristics_block = block.find(data-tab-id="distinctive")
        # try:
        #     product_characteristics_items = product_characteristics_block.select_one('table').select('tr')
        # except:
        #     product_characteristics_items = ''

        # if product_characteristics_items:
        #     product_characteristics = '{ '
        #     if len(product_characteristics_items[0].select('td')) > 1: 
        #         product_characteristics += '"main": { '
        #     # is_cell_header_previous = False
        #     for i, row in enumerate(product_characteristics_items):
        #         cells = row.select('td')
                
        #         if len(cells) < 1: continue
        #         is_cell_header = len(cells) == 1;
        #         # product_characteristics  += ' %s: ' % is_cell_header_previous
        #         if is_cell_header:
        #             # if i > 1:
        #             product_characteristics += '"%s": { ' % (cells[0].get_text().strip())
        #             # else:
        #             #     product_characteristics += '{ "%s": { ' % cells[0].get_text().strip()
        #         else:
        #             # print(cells)
        #             product_characteristics += '"%s": "%s ", ' % (cells[0].get_text().strip(), cells[1].get_text().strip()) 
        #             if i < len(product_characteristics_items) - 1:
        #                 if len(product_characteristics_items[i+1].select('td')) == 1:
        #                     product_characteristics = re.sub(r',\s$', '', product_characteristics)
        #                     product_characteristics += ' }, '

        #     product_characteristics = re.sub(r',\s$', '', product_characteristics) + ' } }'
        # else:
        #     product_characteristics = ''

        # if not product_characteristics:
        #     logger.debug('no characteristics')
        #     return

        # Product description ----------------------------
        product_description_block = block.select('.productTabs__item')
        # print(product_description_block)

        product_description = '{ '
        for i, item in enumerate(product_description_block):
            outerHTML = str(item)
            # print(i, ": ", outerHTML.find('data-tab-id="distinctive"'))
            # print(i, ": ", outerHTML.find('data-tab-id="1"'))
            if outerHTML.find('data-tab-id="distinctive"') > -1 : key = 'description'
            else:
                if outerHTML.find('data-tab-id="1"') > -1 : key = 'characteristics'
                else: key = '%s' % i
            try:
                product_description += '"%s": "%s", ' % (key, re.sub(r'"', '\\"', item.select_one('div.wrapper').decode_contents()) )
            except:
                 product_description += '"%s": "%s", ' % (key, '')

        product_description = re.sub(r',\s*$', '', product_description) + ' }'

        # product_description = product_description_block.decode_contents()
        product_description = re.sub(r'lazy-src', 'src', product_description)
        product_description = re.sub(r'\s+', ' ', product_description)
        
        # try:
        #     product_description = '"%s"' % re.sub(r'"', '\\"', product_description)
        # except:
        #     product_description = '"%s"' % ''

        # Product summary images ----------------------------
        product_description_images_array = []
        for item in product_description_block:
            product_description_images_array += item.select('img')


        product_description_images = '[ '
        for image in product_description_images_array:
            try:
                product_description_images += '{ "url": "%s", "alt": "%s" },' % ( image.get('lazy-src') if image.get('lazy-src') else image.get('src'), image.get('alt') )
            except:
                product_description_images += '{ "url": "%s", "alt": "%s" },' % ( '','' )

        product_description_images = re.sub(r',\s*$', '', product_description_images) + ' ]'

        # logger.debug('\n%s\n%s\n%s' % (product_description, product_characteristics, product_description_images))
        logger.debug('\n%s\n%s' % (product_description, product_description_images))

        self.ParseResult['product_description'] = product_description
        # self.ParseResult['product_characteristics'] = product_characteristics
        self.ParseResult['product_description_images'] = product_description_images

        self.ParseResult['source_url'] = '"%s"' % self.url

    def save_result(self):
        path = self.result_file_path
        with open(path, 'w', encoding='utf-8') as f:
            f.write('{\n')
            for i, key in enumerate(self.ParseResult):
                f.write( '"%s": %s%s\n' % (key, self.ParseResult[key], '' if i == len(self.ParseResult)-1 else ', ') ) 
            f.write('\n}\n')




    def run(self):
        text = self.load_page()
        if not text: return False
        self.parse_page(text=text)
        self.save_result()



if __name__ == '__main__':
    result_file_path = 'stanki-brands.json'
    source_file_path = 'brands-urls.txt'
    result_folder = 'result-brands/'
    start_index = 0
    end_index = 4000

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

