import os

os.chdir("./Udemy/Python_Angela/second_local/day30")
# FileNotFound
# with open("file.txt") as file:
#     file.read()
# KeyError
# d = {"key": "val"}
# v = d["non_exist_key"]

# IndexError
# fruit_list = ["A", "B", "C"]
# fruit = fruit_list[3]

# TypeError
# text = "abc"
# print(text + 5)

# try:
#     file = open("file.txt")
#     d = {"key": "val"}
#     print(d["non_exist_key"])
#     print(d["key"])

# except FileNotFoundError:
#     file = open("file.txt", "w")
#     file.write("blah blah")
# except KeyError as error_message:
#     print(f"That key {error_message} does not exist")
# else:
#     content = file.read()
#     print(content)
# finally:
#     file.close()
#     print("File was closed")

# height = float(input("Height: "))
# weight = int(input("Weight: "))

# if height > 3:
#     raise ValueError("Human Height should not be over 3 meters")

# bmi = weight / height**2
# print(bmi)

# IndexError Handling
fruits = ["Apple", "Pear", "Orange"]


def make_pie(index):
    try:
        fruit = fruits[index]
    except IndexError:
        print("Fruit pie")
    else:
        print(fruit + " pie")
