# password-gen, for, range

import random
fruits = ["apple", "peach", "pear"]
for fruit in fruits:
    print(fruit)
    print(fruit + " Pie")
    print(fruits)
print(fruits)
#
# 🚨 Don't change the code below 👇
student_heights = input("Input a list of student heights ").split()
for n in range(0, len(student_heights)):
    student_heights[n] = int(student_heights[n])
# 🚨 Don't change the code above 👆


# Write your code below this row 👇

sum = 0
count = 0
for height in student_heights:
    sum += height
    count += 1

print(round(sum / count))
#
# 🚨 Don't change the code below 👇
student_scores = input("Input a list of student scores ").split()
for n in range(0, len(student_scores)):
    student_scores[n] = int(student_scores[n])
print(student_scores)
# 🚨 Don't change the code above 👆

# Write your code below this row 👇
highest = 0

for score in student_scores:
    if score > highest:
        highest = score

print(f"The highest score in the class is: {highest}")
#
for num in range(1, 10, 3):
    print(num)
total = 0
for num in range(1, 101):
    total += num
print(total)
#
# Write your code below this row 👇

total = 0
for num in range(0, 101, 2):
    total += num
print(total)

total2 = 0
for num in range(0, 101):
    if num % 2 == 0:
        total2 += num
print(total2)
#
# Write your code below this row 👇

for num in range(1, 101):
    if num % 3 == 0 and num % 5 == 0:
        print("FizzBuzz")
    elif num % 3 == 0:
        print("Fizz")
    elif num % 5 == 0:
        print("Buzz")
    else:
        print(num)
#
# Password Generator Project
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
           'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters = int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

# Eazy Level - Order not randomised:
# e.g. 4 letter, 2 symbol, 2 number = JduE&!91

password = ""

for cnt in range(0, nr_letters):
    rd_num = random.randint(0, len(letters) - 1)
    password += letters[rd_num]
for cnt in range(0, nr_symbols):
    rd_num = random.randint(0, len(symbols) - 1)
    password += symbols[rd_num]
for cnt in range(0, nr_numbers):
    rd_num = random.randint(0, len(numbers) - 1)
    password += numbers[rd_num]

print(f"Your password is: {password}")


# Hard Level - Order of characters randomised:
# e.g. 4 letter, 2 symbol, 2 number = g^2jk8&P
password2 = []
for cnt in range(0, nr_letters):
    password2.append(random.choice(letters))
for cnt in range(0, nr_symbols):
    password2.append(random.choice(symbols))
for cnt in range(0, nr_numbers):
    password2.append(random.choice(numbers))


random.shuffle(password2)
# password2 = "".join(password2)
hard_password = ''
for str in password2:
    hard_password += str
print(f"Your password is: {hard_password}")
