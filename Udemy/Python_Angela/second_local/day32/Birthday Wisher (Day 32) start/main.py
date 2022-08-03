# import smtplib

# my_email = "ryuseongryong@gmail.com"
# password = ""

# with smtplib.SMTP("smtp.gmail.com") as connection:
#     connection.starttls()
#     connection.login(user=my_email, password=password)
#     connection.sendmail(
#         from_addr=my_email,
#         to_addrs=my_email,
#         msg="Subject:Hello\n\nThis is the body of my email.",
#     )
import datetime as dt

now = dt.datetime.now()
year = now.year
month = now.month
day_of_week = now.weekday()
print(now, year, month, day_of_week)

date_of_birth = dt.date(year=1993, month=9, day=25)
print(date_of_birth)
