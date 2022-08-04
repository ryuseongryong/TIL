import os, datetime, pandas, random, smtplib

os.chdir("./Udemy/Python_Angela/second_local/day32/birthday-wisher-extrahard-start")




now = datetime.datetime.now()
today = (now.month, now.day)


data = pandas.read_csv("birthdays.csv")

birthdays_dict = {
    (data_row["month"], data_row["day"]): data_row
    for (index, data_row) in data.iterrows()
}

if today in birthdays_dict:
    birthday_person = birthdays_dict[today]
    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP()


##################### Extra Hard Starting Project ######################


# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.
