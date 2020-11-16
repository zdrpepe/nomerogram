import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re


URL = 'https://www.nomerogram.ru/'
SER1 = 'К'
SER2 = 'ОТ'
REGION = '154'
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome()


def dromChecker(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, features="html.parser")

    resp = soup.find('span', text='Автомобиль продан')
    if resp is None:
        return True
    else:
        return False


def parser(num):
    driver.get(URL)
    driver.find_element_by_name('series1').send_keys(SER1)
    driver.find_element_by_name('number').send_keys(num)
    driver.find_element_by_name('series2').send_keys(SER2)
    driver.find_element_by_name('region').send_keys(REGION)
    driver.find_element_by_xpath('/html/body/div/main/form/div[3]/button').click()
    time.sleep(3)
    res = driver.page_source
    soup = BeautifulSoup(res, features="html.parser")

    infoBlock = soup.find('div', class_='ng-card')
    adts = infoBlock.find_all_next('div', class_='ng-card__origin ng-text_gray')
    for adt in adts:
        if 'drom' in (str(adt.text).strip()):
            if dromChecker(str(adt.text).strip()):
                print(SER1 + str(num) + SER2 + REGION + ' <---------> ' + str(adt.text).strip())

    # driver.close()

if __name__ == '__main__':
    for num in range(1, 1000):
        parser(f'{num:03}')

    driver.close()
