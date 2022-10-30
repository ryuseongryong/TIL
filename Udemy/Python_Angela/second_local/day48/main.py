import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By


load_dotenv()
os.chdir("./Udemy/Python_Angela/second_local/day48")

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
# driver.get(
#     "https://www.amazon.com/Instant-Pot-Multi-Use-Programmable-Pressure/dp/B00FLYWNYQ?ref_=Oct_d_obs_d_3117954011&pd_rd_w=ArEhS&content-id=amzn1.sym.9aa64228-a828-4242-9935-e693c0cc3357&pf_rd_p=9aa64228-a828-4242-9935-e693c0cc3357&pf_rd_r=NVBK0GMQDFDAQKS3RW88&pd_rd_wg=yEd3W&pd_rd_r=1c555357-a10e-47e7-b381-106601861143&pd_rd_i=B00FLYWNYQ"
# )

# price = driver.find_element(By.CLASS_NAME, "priceToPay")

# print(price.text)
# driver.close()

driver.get("https://www.python.org/")
# search_bar = driver.find_element(By.NAME, "q")
# print(search_bar.tag_name)
# print(search_bar.get_attribute("placeholder"))

# logo = driver.find_element(By.CLASS_NAME, "python-logo")
# print(logo.size)

# documentation_link = driver.find_element(By.CSS_SELECTOR, ".documentation-widget a")
# print(documentation_link.text)

# bug_link = driver.find_element(By.XPATH, '//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
# print(bug_link.text)

event_times = driver.find_elements(By.CSS_SELECTOR, ".event-widget time")
event_names = driver.find_elements(By.CSS_SELECTOR, ".event-widget li a")
events = {}

for n in range(len(event_times)):
    events[n] = {"time": event_times[n].text, "name": event_names[n].text}

print(events)

driver.quit()
