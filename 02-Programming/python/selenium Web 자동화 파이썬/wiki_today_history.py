from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from datetime import datetime
import csv

file_name = f'wiki_today({str(datetime.today())[:10]}).csv'

file = open(file_name, 'w', newline='')
write = csv.writer(file)

driver = webdriver.Chrome(r'/Users/seongryongryu/Desktop/TIL/selenium Web 자동화 파이썬/chromedriver')
url = 'https://ko.wikipedia.org/wiki/%EC%9C%84%ED%82%A4%EB%B0%B1%EA%B3%BC:%EC%98%A4%EB%8A%98%EC%9D%98_%EC%97%AD%EC%82%AC'
driver.get(url)
driver.maximize_window()
action = ActionChains(driver)

a = driver.find_element_by_css_selector('#hslice-1').text
write.writerow([a])

driver.close()