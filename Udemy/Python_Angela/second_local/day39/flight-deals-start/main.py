from data_manager import DataManager

print("start main")
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

if sheet_data[0]["iataCode"] == "Test":

    for row in sheet_data:
        from flight_search import FlightSearch

        flight_search = FlightSearch()

        print(flight_search.get_destination_code(row["city"]))

        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet_data:\n {sheet_data}")

    data_manager.destination_data = sheet_data
    data_manager.update_destination_iatacode()
print("end of main")
