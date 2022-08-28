from email import header
import os
import requests
from dotenv import load_dotenv

os.chdir("./Udemy/Python_Angela/second_local/day38")
load_dotenv()

GENDER = "man"
WEIGHT = "75"
HEIGHT = "175"
AGE = "30"

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Which exercises you did? ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

res = requests.post(exercise_endpoint, json=params, headers=headers)
print(res.json(), res)