import os

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.getenv("API_KEY")


class FlightSearch:
    def get_destination_code(self, city_name):
        code = "Test"
        return code
