import os
import csv
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


data = pandas.read_csv("weather_data.csv")
print(data["temp"])
