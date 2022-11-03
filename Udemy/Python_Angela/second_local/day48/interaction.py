import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


load_dotenv()
os.chdir("./Udemy/Python_Angela/second_local/day48")

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

# driver.get("https://ko.wikipedia.org/wiki/Main_Page")
driver.get("https://secure-retreat-92358.herokuapp.com/")

first_name = driver.find_element(By.NAME, "fName")
first_name.send_keys("Seongryong")
last_name = driver.find_element(By.NAME, "lName")
last_name.send_keys("Ryu")
email = driver.find_element(By.NAME, "email")
email.send_keys("ryuseongryong@gmail.com")

submit = driver.find_element(By.CSS_SELECTOR, "form button")
submit.click()

# article_count = driver.find_element(By.CSS_SELECTOR, ".nomobile a")
# article_count.click()

# community = driver.find_element(By.LINK_TEXT, "사랑방")
# community.click()

# search = driver.find_element(By.NAME, "search")
# search.send_keys("Python")
# search.send_keys(Keys.ENTER)

# driver.quit()
