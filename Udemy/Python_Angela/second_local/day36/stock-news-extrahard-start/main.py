import requests, os
from dotenv import load_dotenv
from twilio.rest import Client

os.chdir("./Udemy/Python_Angela/second_local/day36")
load_dotenv()


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_PHONE = os.getenv("FROM_PHONE")
TO_PHONE = os.getenv("TO_PHONE")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

stock_res = requests.get(STOCK_ENDPOINT, params=stock_params)
data = stock_res.json()["Time Series (Daily)"]
data_list = [val for (key, val) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_data_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_data_closing_price)

diff_price = float(yesterday_closing_price) - float(
    day_before_yesterday_data_closing_price
)

up_down = None
if diff_price > 0:
    up_down = "떡상!"
else:
    up_down = "떡락!"

diff_pct = round((diff_price / float(yesterday_closing_price)) * 100)
print(diff_price)
print(diff_pct)

if abs(diff_pct) > 0:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_res = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_res.json()["articles"]

    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [
        f"{STOCK}:  {up_down}{diff_pct}%\nHeadline: {article['title']}. \nBrief: {article['description']}"
        for article in three_articles
    ]
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=FROM_PHONE,
            to=TO_PHONE,
        )
