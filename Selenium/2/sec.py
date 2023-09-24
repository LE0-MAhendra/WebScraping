import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json

website = "https://www.audible.in/search"
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))
driver.get(website)
# Scroll down to load more products
scroll_pause_time = 2  # Adjust as needed
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find all product elements on the page
product_divs = driver.find_elements(By.CLASS_NAME, "adbl-impression-item")

data = []
for prod in product_divs:
    title = prod.find_element(By.CLASS_NAME, "bc-heading").text
    author = prod.find_element(By.CLASS_NAME, "authorLabel").text
    time = prod.find_element(By.CLASS_NAME, "runtimeLabel").text
    extracted = {
        'title': title,
        'author': author,
        'time': time,
    }
    data.append(extracted)

with open('Products.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

driver.quit()
