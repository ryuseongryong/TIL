import os

os.chdir("./Udemy/Python_Angela/second_local/day30")
# FileNotFound
# with open("file.txt") as file:
#     file.read()
try:
    file = open("file.txt")
    d = {"key": "val"}
    print(d["non_exist_key"])
    print(d["key"])

except FileNotFoundError:
    file = open("file.txt", "w")
    file.write("blah blah")
except KeyError as error_message:
    print(f"That key {error_message} does not exist")
else:
    content = file.read()
    print(content)
finally:
    file.close()
# KeyError
# d = {"key": "val"}
# v = d["non_exist_key"]

# IndexError
# fruit_list = ["A", "B", "C"]
# fruit = fruit_list[3]

# TypeError
# text = "abc"
# print(text + 5)
