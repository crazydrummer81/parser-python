import logging
import collections
import re
import csv
import json
import time

import requests
import bs4


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')

class Client:

    ParseResult = []

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

        container = soup.select('div.catalog__product')
        for block in container:
            self.parse_product_cards(block=block)

    def parse_product_cards(self, block):
        product_cards = block.select('a.product')
        # logger.info(product_cards)
        urls = []
        for item in product_cards:
            a = item.get('href')
            urls.append(a)
            # print(a)
        # print(urls)

        # logger.debug('\n%s', urls)

        self.ParseResult.append(urls)
    

    def save_result(self):
        path = self.result_file_path
        with open(path, 'w', encoding='utf-8') as f:
            for urls in self.ParseResult:
                f.write( "\n".join(urls) ) 
                # f.write( str(urls) ) 
                f.write( '\n') 
                # print(self.ParseResult[i])




    def run(self):
        text = self.load_page()
        if not text: return False
        self.parse_page(text=text)
        self.save_result()



if __name__ == '__main__':
    source_file_path = 'pages-to-parse.txt'
    result_folder = ''
    result_file_path = 'products-links.txt'

    print('>>> START <<<')

    start_index = 0
    end_index = 500

    counter = start_index
    with open(source_file_path, 'r', encoding='utf-8') as f:
        while True:
            counter += 1
            url = f.readline().strip()
            if counter < start_index: continue
            if counter > end_index: break
            if len(url) == 0: break
            parser = Client(url, result_folder + result_file_path)
            print(f'NUMBER: {counter:05d}')
            parser.run()
            time.sleep(1)

