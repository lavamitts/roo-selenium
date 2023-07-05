from calendar import c
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from classes.database import Database


load_dotenv('.env')
min_code = os.getenv('MIN_CODE')
max_code = os.getenv('MAX_CODE')
screenshot_folder = os.path.join(os.getcwd(), "screenshots")
ff_options = Options()
ff_options.headless = True

# Get commodities:
sql = """
with cer as (
	select goods_nomenclature_item_id, left(goods_nomenclature_item_id, 2) as chapter,
	validity_end_date
	from goods_nomenclatures
	where producline_suffix = '80'
	and right(goods_nomenclature_item_id, 2) != '00'
    and goods_nomenclature_item_id >= %s
    and goods_nomenclature_item_id <= %s
	and (validity_end_date >= current_date or validity_end_date is null)
    and validity_start_date::date <= current_date
)
select distinct on (chapter)
chapter, goods_nomenclature_item_id, validity_end_date
from cer
order by chapter, goods_nomenclature_item_id desc;
"""
d = Database()
params = [
    min_code,
    max_code
]
rows = d.run_query(sql, params)
countries = [
    "AT",
    "AL",
    "CA",
    "KR",
    "KE",
    "SC",
    "JP",
    "CR",
    "PE",
    "CM",
    "AG",
    "CL",
    "CI",
    "EG",
    "FO",
    "GE",
    "GH",
    "IS",
    "IL",
    "XK",
    "JO",
    "LB",
    "MX",
    "CH",
    "MD",
    "MA",
    "MK",
    "FJ",
    "PS",
    "SG",
    "XS",
    "BW",
    "TN",
    "TR",
    "UA",
    "VN",
    "AI",
    "AF"
]

countries = [
    "MD",
    "MA",
    "MK",
    "FJ",
    "PS",
    "SG",
    "XS",
    "BW",
    "TN",
    "UA",
    "VN",
    "AI",
    "AF"
]

countries = [
    "VN"
]
log_file = open("logs/log.txt", "w+")
for country in countries:
    screen_shot_folder_by_country = os.path.join(screenshot_folder, country)
    if not os.path.isdir(screen_shot_folder_by_country):
        os.mkdir(screen_shot_folder_by_country)

    index = -1
    for row in rows:
        index += 1
        commodity = row[1]
        url = "http://localhost:3000/roo/product_specific_rules/{commodity}/{country}".format(
            commodity=commodity,
            country=country
        )
        screenshot_file = os.path.join(screen_shot_folder_by_country, "{commodity}.png".format(
            commodity=commodity
        ))
        driver = webdriver.Firefox(options=ff_options)
        driver.get(url)
        driver.save_screenshot(screenshot_file)
        print("Processing commodity {commodity} on country {country}".format(
            commodity=commodity,
            country=country
        ))
        elems = driver.find_elements(By.CLASS_NAME, "psr_for_selenium_label")
        for elem in elems:
            elem_text = elem.text.strip()
            if len(elem_text) < 5:
                print("Missing content", commodity, country)
                log_file.write("Missing content for commodity {commodity} on country {country}.".format(
                    commodity=commodity,
                    country=country
                ))

        driver.close()
        driver = None

log_file.close()
