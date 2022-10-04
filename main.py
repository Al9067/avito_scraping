from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import traceback
import csv
import unicodedata

URL = 'https://www.avito.ru/arhangelsk/kvartiry/prodam/do-3-mln-rubley-ASgBAgECAUSSA8YQAUXGmgwXeyJmcm9tIjowLCJ0byI6MzAwMDAwMH0?f=ASgBAQECAkSSA8YQqu4OyKHjAgJA5hYU5vwBrL4NFKTHNQFFxpoMF3siZnJvbSI6MCwidG8iOjMwMDAwMDB9&p='

s = Service('C:/Users/ai887/Documents/study_projects/web_scraping_python/avito-scraping/chromedriver.exe')

headers = {"user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"}

START_PAGE = 1
STOP_PAGE = 2


def get_flats_info(url):
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    try:
        driver.get(url=url)
        time.sleep(3)
        with open('flats.csv', 'a', encoding='utf-8') as flats_csv:
            writer = csv.writer(flats_csv, delimiter=';')
            for page in range(START_PAGE, STOP_PAGE + 1):
                next_page = driver.find_element(By.XPATH,
                                                "//span[@class='pagination-item-JJq_j pagination-item_arrow-Sttbt']")
                flats = driver.find_elements(By.XPATH, "//div[@class='iva-item-content-rejJg']")
                for flat in flats[:3]:
                    flat.click()
                    driver.switch_to.window(driver.window_handles[-1])
                    try:
                        flat_title = unicodedata.normalize("NFKD", driver.find_element(By.XPATH, "//span[@class='title-info-title-text']").text)
                    except NoSuchElementException:
                        flat_title = None
                        print('flat_title is undefined')
                    try:
                        flat_price = unicodedata.normalize("NFKD", driver.find_element(By.XPATH,
                                                             "//span[@class='js-item-price style-item-price-text-2u_qK text-text-1PdBw text-size-xxl-1Uoae']").text)
                    except NoSuchElementException:
                        flat_price = None
                        print('flat_price is undefined')
                    try:
                        flat_description = unicodedata.normalize("NFKD",driver.find_element(By.XPATH, "//ul[@class='params-paramsList-2PiKQ']").text)
                    except NoSuchElementException:
                        flat_description = None
                        print('flat_description is undefined')
                    try:
                        flat_url = unicodedata.normalize("NFKD", str(driver.current_url))
                    except NoSuchElementException:
                        print('flat_url is undefined')
                    print(flat_title, flat_price, flat_description, flat_url)
                    writer.writerow([flat_title, flat_price, flat_description, flat_url])
                    time.sleep(3)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                next_page.click()
                time.sleep(3)
    except NoSuchElementException:
        print('Some element not defined')
        traceback.print_exc()
    finally:
        driver.close()
        driver.quit()


get_flats_info(f'{URL}{START_PAGE}')


