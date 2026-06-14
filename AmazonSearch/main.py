from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CDM
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

browser = webdriver.Chrome(
    service=ChromeService(CDM().install()),
    options=Options().add_argument('--headless')
)
browser.maximize_window()

browser.implicitly_wait(10)

url = "https://www.amazon.in/"
browser.get(url)
# key = input("Enter what you want to search:")
key = "Iphone 14 Pro"
search_key = browser.find_element(By.CSS_SELECTOR, "input[name='field-keywords']")
search_key.send_keys(key)
search_key.submit()

data_list = []

names = browser.find_elements(By.CSS_SELECTOR, "span[class='a-size-medium a-color-base a-text-normal']")
prices = browser.find_elements(By.CSS_SELECTOR, "span[class='a-price-whole']")

name_list = [name.text.replace(",","-") for name in names]
price_list = [price.text.replace(",","") for price in prices]

for n, p in zip(name_list, price_list):
    data_list.append({"name": n, "price": p})

print(data_list)
with open(key+".json", "w") as file:
    json.dump(data_list, file, indent=4)
browser.quit()