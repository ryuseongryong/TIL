import os
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()
os.chdir("./Udemy/Python_Angela/second_local/day48")

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get("https://naver.com")
# driver.close()
driver.quit()
