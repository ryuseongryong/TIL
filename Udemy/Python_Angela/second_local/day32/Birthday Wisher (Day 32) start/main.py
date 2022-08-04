from calendar import weekday
import smtplib
import datetime as dt
import random
import os

os.chdir("./Udemy/Python_Angela/second_local/day32/Birthday Wisher (day 32) start")

MY_EMAIL = "ryuseongryong@gmail.com"
MY_PASSWORD = ""


now = dt.datetime.now()
weekday = now.weekday()
if weekday == 3:
    with open("quotes.txt") as quote_file:
        all_quotes = quote_file.readlines()
        quote = random.choice(all_quotes)

    print(quote)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Daily Motivation\n\n{quote}",
        )
