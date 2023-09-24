
"""
element = driver.find_element(By.ID, "passwd-id")
element = driver.find_element(By.NAME, "passwd")
element = driver.find_element(By.XPATH, "//input[@id='passwd-id']")
element = driver.find_element(By.CSS_SELECTOR, "input#passwd-id")
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
website = "https://www.adamchoi.co.uk/overs/detailed"
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))
driver.get(website)

############## CLICKING ON A BUTTON AND CHECKING DATA #############################
matches_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//label[@analytics-event='All matches']"))
)
matches_btn.click()
########### SELECTING A OPTION IN DROPDOWN MENU AND SELECT A OPTION ###################
options = Select(driver.find_element(By.ID, 'country'))
options.select_by_visible_text('Spain')

# Wait for the table rows to load (you may adjust the timeout as needed)
table_tr = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
)
data = []

for table in table_tr:
    date = table.find_element(By.XPATH, "//tr/td[1]").text
    hometeam = table.find_element(By.XPATH, "//tr/td[2]").text
    score = table.find_element(By.XPATH, "//tr/td[3]").text
    awayteam = table.find_element(By.XPATH, "//tr/td[4]").text
    extracted = {
        'date': date,
        'HomeTeam': hometeam,
        'Score': score,
        'AwayTeam': awayteam,
    }
    data.append(extracted)
print(len(table_tr))
with open('tabledata.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
