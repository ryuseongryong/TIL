# function print, input, len, \n, variable
print("Hello World!")

print("Day 1 - Python Print Function")
print("The function is declared like this:")
print("print('what to print')")

print("Hello World!\nHello World!\nHello World!")
print("Hello" + " " + "Seongryong")

print("Day 1 - String Manipulation")
print('String Concatenation is done with the "+" sign.')
print('e.g. print("Hello " + "world")')
print("New lines can be created with a backslash and n.")

# input() will get user input in console
# Then print() will print the word "Hello" and the user input
print("Hello " + input("What is your name?"))

#
print(len(input("What is your name? ")))

#
name = "Jack"
print(name)

name = "Ryuseongryong"
print(name)

name = input("What is your name?")
length = len(name)
print(length)
#
# 🚨 Don't change the code below 👇
a = input("a: ")
b = input("b: ")
# 🚨 Don't change the code above 👆

####################################
# Write your code below this line 👇
temp = a
a = b
b = temp

# Write your code above this line 👆
####################################

# 🚨 Don't change the code below 👇
print("a: " + a)
print("b: " + b)
#
# 1. Create a greeting for your program.
print("Welcome to the Band name Generator!")

# 2. Ask the user for the city that they grew up in.
city = input("What's name of the city you grew up in?\n")

# 3. Ask the user for the name of a pet.
pet = input("What's your pet's name?\n")

# 4. Combine the name of their city and pet and show them their band name.
band_name = city + " " + pet

# 5. Make sure the input cursor shows on a new line, see the example at:
pet = input("Your band name could be " + band_name)
#   https://replit.com/@appbrewery/band-name-generator-end
