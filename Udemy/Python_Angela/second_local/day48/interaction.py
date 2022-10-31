import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By


load_dotenv()
os.chdir("./Udemy/Python_Angela/second_local/day48")

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

driver.get("https://ko.wikipedia.org/wiki/Main_Page")
article_count = driver.find_element(By.CSS_SELECTOR, ".nomobile a")
print(article_count.text)

driver.quit()
