# randomisation(Python - Mersenne Twister), List, IndexError, nested List

#
# Write your code below this line 👇
# Hint: Remember to import the random module first. 🎲

import random

t_or_h = round(random.random())

if t_or_h:
    print('Tails')
else:
    print('Heads')
#
# Split string method
names_string = input("Give me everybody's names, separated by a comma. ")
names = names_string.split(", ")
# 🚨 Don't change the code above 👆

# Write your code below this line 👇

length = len(names) - 1

# == random_choice = random.choice(names)
random_choice = names[random.randint(0, length)]
print(f"{random_choice} is going to buy the meal today.")
#
# 🚨 Don't change the code below 👇
row1 = ["⬜️", "⬜️", "⬜️"]
row2 = ["⬜️", "⬜️", "⬜️"]
row3 = ["⬜️", "⬜️", "⬜️"]
map = [row1, row2, row3]
print(f"{row1}\n{row2}\n{row3}")
position = input("Where do you want to put the treasure? ")
# 🚨 Don't change the code above 👆

# Write your code below this row 👇

col = int(position[0]) - 1
row = int(position[1]) - 1

map[row][col] = 'x'

# Write your code above this row 👆

# 🚨 Don't change the code below 👇
print(f"{row1}\n{row2}\n{row3}")

#
rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

# Write your code below this line 👇

R_P_S = [rock, paper, scissors]


user_int = int(
    input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors."))
if user_int > 2:
    print("invalid int")

else:
    user_selection = R_P_S[user_int]

    random_int = random.randint(0, 2)
    computer_selection = R_P_S[random_int]

    print(user_selection)

    print("Computer chose:")
    print(computer_selection)

    if user_int == random_int:
        print("You draw")
    elif (user_int == random_int - 1) or (user_int == random_int + 2):
        print("You lose")
    # elif (user_int == random_int + 1) or (user_int == random_int - 2):
    else:
        print("You Win")
