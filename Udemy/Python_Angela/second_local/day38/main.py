import os
import requests
from dotenv import load_dotenv
from datetime import datetime

os.chdir("./Udemy/Python_Angela/second_local/day38")
load_dotenv()

GENDER = "man"
WEIGHT = "75"
HEIGHT = "175"
AGE = "30"

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Which exercises you did? ")

headers = {"x-app-id": APP_ID, "x-app-key": API_KEY}

params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
}

res = requests.post(exercise_endpoint, json=params, headers=headers)
print(res.json(), res)
data = res.json()

today = datetime.now().strftime("%Y/%m/%d")
now_time = datetime.now().strftime("%X")

for exercise in data["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheet_res = requests.post(API_URL, json=sheet_inputs)

    print(sheet_res.text)
