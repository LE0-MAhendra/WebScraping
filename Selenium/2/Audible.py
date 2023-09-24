"""
element = driver.find_element(By.ID, "passwd-id")
element = driver.find_element(By.NAME, "passwd")
element = driver.find_element(By.XPATH, "//input[@id='passwd-id']")
element = driver.find_element(By.LINK_TEXT, "link text")
element = driver.find_element(By.PARTIAL_LINK_TEXT, "partial link text")
element = driver.find_element(By.TAG_NAME, "tag name")
element = driver.find_element(By.CLASS_NAME, "class name")
element = driver.find_element(By.CSS_SELECTOR, "input#passwd-id")
"""
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
website = "https://www.audible.in/adblbestsellers?ref_pageloadid=jB5cmyaiLrYd2ikP&ref=a_search_t1_navTop_pl1cg0c1r0&pf_rd_p=88b2dc24-01ab-437a-bf8e-1faf3da486fb&pf_rd_r=F8CKCGEGY4DVT4VJZ73J&pageLoadId=xM9hse1o1vMPolL7&creativeId=2e6787a2-0cd0-4a6e-afe0-05766cd505e5"
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))
driver.get(website)
############# PAGINATION/Multipages #########################

pagination = driver.find_element(
    By.XPATH, "//ul[contains(@class,'pagingElements')]")
pages = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(pages[-2].text)
current = 1
data = []
while current <= last_page:
    all_products_div = driver.find_element(
        By.CLASS_NAME, "adbl-impression-container")
    product_div = all_products_div.find_elements(
        By.XPATH, '//li[contains(@class, "productListItem")]'
    )
    for prod in product_div:
        title = prod.find_element(
            By.XPATH, './/li/h3[contains(@class, "bc-heading")]/a').text
        author = prod.find_element(
            By.XPATH, './/li[contains(@class,"authorLabel")]//span//a').text
        time = prod.find_element(
            By.XPATH, './/li[contains(@class,"runtimeLabel")]//span').text
        extracted = {
            'title': title,
            'author': author,
            'time': time,
        }
        data.append(extracted)
    current += 1
    try:
        next_btn = driver.find_element(
            By.XPATH, "//span[contains(@class,'nextButton')]")
        next_btn.click()
    except:
        pass


with open('Bestsellers.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
