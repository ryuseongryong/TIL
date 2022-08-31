import requests, os
from dotenv import load_dotenv

os.chdir("./Udemy/Python_Angela/second_local/day39/filght-deals-start")
load_dotenv()


SHEETY_ENDPOINT = os.getenv("API_URL")


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    pass
