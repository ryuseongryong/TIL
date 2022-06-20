from importlib.resources import contents


file = open("file.txt")
contents = file.read()
print(contents)
