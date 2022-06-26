import os
import pandas

# print(os.getcwd())
os.chdir("./Udemy/Python_Angela/second_local/day25")


# with open("weather_data.csv") as data_file:
#     data = data_file.readlines()
#     print(data)


# with open("weather_data.csv") as data_file:
#     data = csv.reader(data_file)
#     temperatures = []
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(row[1])

#     print(temperatures)

# Pandas functions
# data = pandas.read_csv("weather_data.csv")
# # print(type(data))
# # print(type(data["temp"]))

# data_dict = data.to_dict()
# # print(data_dict)

# temp_list = data["temp"].to_list()
# # print(temp_list)

# # temp_avg = sum(temp_list) / len(temp_list)
# # print(temp_avg)
# # print(data["temp"].mean())

# temp_max = data["temp"].max()
# # print(temp_max)

# # Get Data in Columns
# # print(data["condition"])
# # print(data.condition)

# # Get Data in Row
# monday = data[data.day == "Monday"]
# # print(row_monday)

# row_max_temp = data[data.temp == temp_max]
# # print(row_max_temp)

# monday_temp_cel = int(monday.temp)
# monday_temp_fah = (monday_temp_cel * 9 / 5) + 32
# print(monday_temp_cel, monday_temp_fah)

# # Create a DataFrame from Scratch
# data_dict = {"students": ["Amy", "James", "Angela"], "scores": [76, 56, 65]}
# data = pandas.DataFrame(data_dict)
# data.to_csv("new_data.csv")

# Central Park Squirrel Census
data = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
gray_squirrels_count = len(data[data["Primary Fur Color"] == "Gray"])
cinnamon_squirrels_count = len(data[data["Primary Fur Color"] == "Cinnamon"])
black_squirrels_count = len(data[data["Primary Fur Color"] == "Black"])
print(gray_squirrels_count)
print(cinnamon_squirrels_count)
print(black_squirrels_count)

data_dict = {
    "Fur Color": ["Gray", "Cinnamon", "Black"],
    "Count": [gray_squirrels_count, cinnamon_squirrels_count, black_squirrels_count],
}

df = pandas.DataFrame(data_dict)
df.to_csv("squirrel_count.csv")
