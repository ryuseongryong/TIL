# Data Types

# String

"Hello"[4]

print("123" + "456")

# Integer

print(123 + 456)

123_456_789

# Float

3.14159

# Boolean

True
False

#str, int, float
num_char = len(input("what is your name?"))
new_num_char = str(num_char)
print("your name is " + new_num_char + "characters!")

a = float(123)
print(type(a))

print(70 + float("100.5"))
print(str(70) + str(231))

#
# 🚨 Don't change the code below 👇
two_digit_number = input("Type a two digit number: ")
# 🚨 Don't change the code above 👆

####################################
# Write your code below this line 👇

sum = int(two_digit_number[0]) + int(two_digit_number[1])

print(sum)

# PEMDAS
#Parentheses - Exponents - Multiplication - Division - Addition - Subtraction
# 괄호 - 지수 - 곱셈 - 나눗셈 - 덧셈 - 뺄셈

# 🚨 Don't change the code below 👇
height = input("enter your height in m: ")
weight = input("enter your weight in kg: ")
# 🚨 Don't change the code above 👆

# Write your code below this line 👇


h = float(height)
w = float(weight)

bmi = w / h**2
bmi_as_int = int(bmi)
print(bmi_as_int)
#
print(round(8 / 3, 2))
print(8 // 3)
print(type(8 // 3))
print(type(8 / 3))

score = 0
height = 1.8
isWinning = True
score += 1

# f-String
print(
    f"your score is {score}, your height is {height}, you are winning is {isWinning}")
#
# 🚨 Don't change the code below 👇
age = input("What is your current age?")
# 🚨 Don't change the code above 👆

# Write your code below this line 👇
last = 90 - int(age)

last_days = last * 365
last_weeks = last * 52
last_months = last * 12

print(
    f"you have {last_days} days, {last_weeks} weeks and {last_months} months left.")
#
# If the bill was $150.00, split between 5 people, with 12% tip.

# Each person should pay (150.00 / 5) * 1.12 = 33.6
# Format the result to 2 decimal places = 33.60

# Tip: There are 2 ways to round a number. You might have to do some Googling to solve this.💪

# Write your code below this line 👇
print("Welcome to the tip calculator!")
total_bill = input("What was the total bill? ")
tip_percent = input("How much tip would you like to give? 10, 12, or 15? ")
people_spliting = input("How many people to split the bill? ")

total_bill_as_float = round(float(total_bill[1:]), 2)
tip_percent_as_float = 1 + int(tip_percent) / 100
people_spliting_as_int = int(people_spliting)

result = round(total_bill_as_float * tip_percent_as_float /
               people_spliting_as_int, 2)

print(f"Each person should pay: {result}")


# except slice function
# If the bill was $150.00, split between 5 people, with 12% tip.

# Each person should pay (150.00 / 5) * 1.12 = 33.6
# Format the result to 2 decimal places = 33.60

# Tip: There are 2 ways to round a number. You might have to do some Googling to solve this.💪

# Write your code below this line 👇
print("Welcome to the tip calculator!")
total_bill = input("What was the total bill? $")
tip_percent = input("How much tip would you like to give? 10, 12, or 15? ")
people_spliting = input("How many people to split the bill? ")

total_bill_as_float = round(float(total_bill), 2)
tip_percent_as_float = 1 + int(tip_percent) / 100
people_spliting_as_int = int(people_spliting)

result = round(total_bill_as_float * tip_percent_as_float /
               people_spliting_as_int, 2)

print(f"Each person should pay: {result}")

# formating
# If the bill was $150.00, split between 5 people, with 12% tip.
# Each person should pay (150.00 / 5) * 1.12 = 33.6
# Round the result to 2 decimal places.
print("Welcome to the tip calculator!")
bill = float(input("What was the total bill? $"))
tip = int(input("How much tip would you like to give? 10, 12, or 15? "))
people = int(input("How many people to split the bill?"))

tip_as_percent = tip / 100
total_tip_amount = bill * tip_as_percent
total_bill = bill + total_tip_amount
bill_per_person = total_bill / people
final_amount = round(bill_per_person, 2)


# FAQ: How to round to 2 decimal places?
final_amount = "{:.2f}".format(final_amount)

print(f"Each person should pay: ${final_amount}")
