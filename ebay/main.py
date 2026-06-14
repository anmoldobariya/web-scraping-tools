from bs4 import BeautifulSoup as BS
import requests
import pandas
from helper_class import *

class MAINCLASS:
    def __init__(self):
        self.helper = Helper()
        self.urls = []
        self.products = []
        self.product_details = {}
    
    def get_http_response(self, url):
        try:
            response = requests.get(url,timeout=5,allow_redirects=True)
            if response.status_code == 200:
                return response
            else:
                print(f"HTTP request to '{url}' returned status code {response.status_code}")
        except requests.RequestException as e:
            print(f"HTTP request to '{url}' failed: {e}")
        return None

    def extract_product_details(self, soup):
        title = self.helper.get_text_from_tag(soup.find('h1', {"class": "product-title"}))
        # print(title)
        price = self.helper.get_text_from_tag(soup.find('div', {"class": "display-price"}))
        # print(price)
        condition = ''
        container = soup.find('div', {'class':'item-desc'})
        if container:
            for ul_element in container.find_all('ul', {'class': 'item-highlights'}):
                for li in ul_element.find_all('li', {'class': 'item-highlight'}):
                    # print(li)
                    if 'condition' in li.text.lower():
                        condition = self.helper.get_text_from_tag(li.find('span', {"class": "cc-ts-BOLD"}))
                        # print(condition)
                    break

        all_details = soup.find('section', {"class": "product-spectification"})
        # print(all_details)
        details = all_details.find_all('li')
        # print(details)
        for detail in details:
            key = self.helper.get_text_from_tag(detail.find('div', {"class": "s-name"}))
            value = self.helper.get_text_from_tag(detail.find('div', {"class": "s-value"}))
            self.product_details[key] = value
            # print(key, value)
        return title, price, condition
    
    def process_urls(self,url):
        print(f"Processing URL: {url}")
        response = self.get_http_response(url)
        if response:
            soup = BS(response.content, 'lxml')
            title, price, condition = self.extract_product_details(soup)
            self.products.append({
                "name": title,
                "price": price,
                "condition": condition,
                "details": self.product_details
            })
        # print(self.products)

    def run_multiThread(self,function,max_workers,args):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(function, args)

    def multiThread(self):
        self.urls = self.helper.read_json_file("urls.json")
        # print(self.urls)
        self.run_multiThread(self.process_urls, 5, self.urls)

    def write_to_csv(self, file):
        try:
            dataFrame = pandas.DataFrame(self.products)
            with open(file, mode='w', encoding='utf-8') as f:
                dataFrame.to_csv(f, mode = 'a', header=True, index = True)
            print(f"CSV File '{file}' created successfully.")
        except Exception as e:
            print(f"Error writing to CSV file '{file}': {e}")


if __name__ == "__main__":
    main_instance = MAINCLASS()
    main_instance.multiThread()
    main_instance.write_to_csv("Products.csv")