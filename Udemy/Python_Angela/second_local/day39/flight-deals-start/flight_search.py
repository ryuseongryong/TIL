import requests, os

# from dotenv import load_dotenv

# os.chdir("./Udemy/Python_Angela/second_local/day39/flight-deals-start")
# load_dotenv()

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.getenv("API_KEY")


class FlightSearch:
    def get_destination_code(self, city_name):
        code = "Test"
        return code


FlightSearch().get_destination_code()
