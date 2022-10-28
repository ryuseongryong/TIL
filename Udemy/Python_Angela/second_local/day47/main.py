import os, requests
from bs4 import BeautifulSoup
import lxml
import smtplib
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
os.chdir("./Udemy/Python_Angela/second_local/day47")

url = "https://www.amazon.com/Instant-Pot-Multi-Use-Programmable-Pressure/dp/B00FLYWNYQ?ref_=Oct_d_obs_d_3117954011&pd_rd_w=ArEhS&content-id=amzn1.sym.9aa64228-a828-4242-9935-e693c0cc3357&pf_rd_p=9aa64228-a828-4242-9935-e693c0cc3357&pf_rd_r=NVBK0GMQDFDAQKS3RW88&pd_rd_wg=yEd3W&pd_rd_r=1c555357-a10e-47e7-b381-106601861143&pd_rd_i=B00FLYWNYQ"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")
print(soup.prettify())

price = soup.find(class_="a-section a-spacing-none aok-align-center").get_text()
# price = soup.find(id="priceblock_ourprice").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 200

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}",
        )
