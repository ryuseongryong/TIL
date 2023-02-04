from importlib.resources import contents


import os

# a = os.listdir("./Udemy/Python_Angela/second_local/day24/file")
# b = os.getcwd()
c = os.chdir("./Udemy/Python_Angela/second_local/day24/file")

# with open("file.txt") as file:
#     contents = file.read()
#     print(contents)


with open("new_file.txt", "w") as file:
    contents = file.write("New text in new file.")

# with open("file.txt", "a") as file:
#     contents = file.write("\nNew text again.")
