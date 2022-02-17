# Blackjack Capstone Project

############### Blackjack Project #####################
from tkinter import N, Y
from replit import clear
from lib.blackjack_art import logo
import random


# wanna_play = input(
#     "Do you want to play a game of Blackjack? Type 'y' or 'n': ")
# start_game = True

# if wanna_play == 'n':
#     start_game = False


# def get_initial_cards():
#     first = cards.pop(random.randint(0, len(cards)-1))
#     second = cards.pop(random.randint(0, len(cards)-1))
#     return [first, second]


# def get_more_card():
#     return cards.pop(random.randint(0, len(cards) - 1))


# def sum(a, b):
#     return a + b


# while start_game:
#     cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

#     print(logo)
#     your_card = get_initial_cards()
#     com_card = get_initial_cards()
#     your_sum = sum(your_card[0], your_card[1])
#     com_sum = sum(com_card[0], com_card[1])

#     # while get_more_card or sum over 21
#     end_game = False
#     while not end_game:

#         print(f"   Your cards: {your_card}, current score: {your_sum}")
#         print(f"   Computer's first card: {com_card[0]}")

#         if your_sum == 21:
#             end_game = True

#         get_another_card = input(
#             "Type 'y' to get another card, type 'n' to pass: ")

#         if get_another_card == 'y':
#             your_card.append(get_more_card())
#             your_sum = sum(your_sum, your_card[-1])

#             if your_sum > 21:
#                 end_game = True

#         elif get_another_card == 'n':
#             end_game = True

#     print(f"   Your final hand: {your_card}, final score: {your_sum}")
#     print(f"   Computer's final hand: {com_card}, final score: {com_sum}")

#     if your_sum > com_sum and your_sum <= 21:
#         print("You win :)")
#     else:
#         print("You Lose :(")

#     wanna_play = input(
#         "Do you want to play a game of Blackjack? Type 'y' or 'n': ")
#     if wanna_play == 'y':
#         clear()
#     elif wanna_play == 'n':
#         start_game = False
## reference
def deal_card():
    """Returns a random card from the dec."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    card = random.choice(cards)
    return card

def calculate_score(cards):
    """Take a list of cards and return the score calculated from the cards."""
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

def compare(user_score, computer_score):
    if user_score == computer_score:
        return "Draw😌"
    elif computer_score == 0:
        return "Lose, opponent has BlackJack! 🤩"
    elif user_score == 0:
        return "Win with a BlackJack! 😎"
    elif user_score > 21:
        return "You went over. You lose 😭"
    elif computer_score > 21:
        return "Opponent went over. You Win! 😁"
    elif user_score > computer_score:
        return "You Win! 😄"
    else:
        return "You lose 😤"
        

def play_game():
    print(logo)
    user_cards = []
    computer_cards = []
    is_game_over = False

    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())
        # It's Not Like Real. In real environment just One pack of Card is using for a game.
    while not is_game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
        print(f"    Your cards: {user_cards}, current score: {user_score}")
        print(f"    Computer's first card: {computer_cards[0]}")

        if user_score == 0 or computer_score == 0 or user_score > 21:
            is_game_over = True
        else:
            user_should_deal = input("Type 'y' to get another card, type 'n' to pass: ")
            if user_should_deal == 'y':
                user_cards.append(deal_card())
            else:
                is_game_over = True

    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)
        
    print(f"    Your final hand: {user_cards}, final score: {user_score}")
    print(f"    Computer's final hand: {computer_cards}, final score: {computer_score}")
    print(compare(user_score, computer_score))

while input("Do you want to play a game of BlackJack? Type 'y' or 'n': ") == "y":
    clear()
    play_game()