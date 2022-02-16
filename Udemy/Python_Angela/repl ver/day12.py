# scope

################### Scope ####################

enemies = 1

def increase_enemies():
  enemies = 2
  print(f"enemies inside function: {enemies}")

increase_enemies()
print(f"enemies outside function: {enemies}")

# Local Scope

def drink_potion():
  potion_strength = 2
  print(potion_strength)

drink_potion()
# print(potion_strength) error name is not defined

# Global Scope

player_health = 10

def game():
  def drink_potion():
    potion_strength = 2
    print(potion_strength)
    print(player_health)

  drink_potion()
  
print(player_health)

# above is about name space

#
# There is no Block Scope

game_level = 3
def create_enemy():
  enemies = ["Skeleton", "Zombie", "Alien"]
  if game_level < 5:
    new_enemy = enemies[0]

  print(new_enemy)

create_enemy()
#
# Modifying Global Scope
enemies = 1

def increase_enemies():
  # global enemies -> not recommend
  print(f"enemies inside function: {enemies}")
  return enemies + 1

enemies = increase_enemies()
print(f"enemies outside function: {enemies}")
#
# Global Constants

PI = 3.14159
URL = "https://www.google.com"
WHATEVER = "value"
#
#Number Guessing Game Objectives:

# Include an ASCII art logo.
# Allow the player to submit a guess for a number between 1 and 100.
# Check user's guess against actual answer. Print "Too high." or "Too low." depending on the user's answer. 
# If they got the answer correct, show the actual answer to the player.
# Track the number of turns remaining.
# If they run out of turns, provide feedback to the player. 
# Include two different difficulty levels (e.g., 10 guesses in easy mode, only 5 guesses in hard mode).
import random
from lib.guess_number_art import logo

print(logo)

print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

answer = random.randint(1, 100)

print(f"Pssst, the correct answer is {answer}")

def check_difficulty():
  difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ")
  life = 10

  if difficulty == 'easy':
    print("You have 10 attempts remaining to guess the number.")
    return life

  elif difficulty == 'hard':
    print("You have 5 attempts remaining to guess the number.")
    life = 5
    return life
  else:
    print("you've enter wrong word!!")
    check_difficulty()

def guess_process():
  guess = int(input("Make a guess: "))
  return guess

def count_life():
  return life - 1

def check_game_over():
  if life == 0:
    return True
  else:
    return False

def check_answer():

  if guess < answer:
    print("Too low.")
    print("Guess again.")
    print(f"You have {life} attempts remaining to guess the number.")

  elif guess > answer:
    print("Too high.")
    print("Guess again.")
    print(f"You have {life} attempts remaining to guess the number.")

  else:
    print(f"You got it! The answer was {answer}.")
    return True

life = check_difficulty()

while not check_game_over():
  guess = guess_process()
  life = count_life()
  end = check_answer()
  if end:
    break
  if life == 0:
    print(f"fail!! {answer}.")
    break
