from calendar import c
import os
import time 
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select


load_dotenv('.env')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

screenshot_file = "test.png"
ff_options = Options()
ff_options.headless = True
url = "https://{username}:{password}@dev.trade-tariff.service.gov.uk/commodities/8708923500?country=AF".format(
    username=USERNAME,
    password=PASSWORD
)
driver = webdriver.Firefox(options=ff_options)
driver.get(url)
action = ActionChains(driver)
for i in range(0, 2):
    action.key_down(Keys.COMMAND).send_keys('-').key_up(Keys.COMMAND).perform()

elems = driver.find_elements(By.CLASS_NAME, "cookie_accept_all")
if len(elems) > 0:
    elem = elems[0]
    elem.click()
    # time.sleep(0.5)
    elems = driver.find_elements(By.CLASS_NAME, "hide_cookie_panel")
    if len(elems) > 0:
        elem = elems[0]
        elem.click()
        # time.sleep(0.5)

driver.save_screenshot(screenshot_file)
driver.close()
driver = None
