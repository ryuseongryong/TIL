import os, time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

os.chdir("./Udemy/Python_Angela/second_local/day49")
load_dotenv()

ACCOUNT_EMAIL = os.getenv("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")
PHONE = os.getenv("PHONE")

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords=python%20developer&location=London%2C%20England%2C%20United%20Kingdom&redirect=false&position=1&pageNum=0"
)

sign_in_button = driver.find_element(By.CLASS_NAME, "nav__button-secondary")
sign_in_button.click()

# Wait for the next page to load.
time.sleep(5)

email_field = driver.find_element(By.ID, "username")
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)
# ---

time.sleep(5)

apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-s-apply button")
apply_button.click()

# If application requires phone number and the field is empty, then fill in the number.
time.sleep(5)
# phone = driver.find_element(By.CLASS_NAME, "fb-single-line-text__input")
# if phone.text == "":
#     phone.send_keys(PHONE)

# next_button = driver.find_element(By.ID, "ember475")
next_button = driver.find_element(By.CLASS_NAME, "artdeco-button--primary")
next_button.click()

time.sleep(5)

# Submit the application
# submit_button = driver.find_element(By.ID, "ember487")
# submit_button.click()
back_button = driver.find_element(By.CLASS_NAME, "artdeco-button--tertiary")
back_button.click()
