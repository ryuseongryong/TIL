# Blackjack Capstone Project

############### Blackjack Project #####################
from tkinter import Y
from replit import clear
from lib.blackjack_art import logo
import random


wanna_play = input(
    "Do you want to play a game of Blackjack? Type 'y' or 'n': ")
start_game = True

if wanna_play == 'n':
    start_game = False


def get_initial_cards():
    first = cards.pop(random.randint(0, len(cards)-1))
    second = cards.pop(random.randint(0, len(cards)-1))
    return [first, second]


def get_more_card():
    return cards.pop(random.randint(0, len(cards) - 1))


def sum(a, b):
    return a + b


while start_game:
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    print(logo)
    your_card = get_initial_cards()
    com_card = get_initial_cards()
    your_sum = sum(your_card[0], your_card[1])
    com_sum = sum(com_card[0], com_card[1])

    # while get_more_card or sum over 21
    end_game = False
    while not end_game:

        print(f"   Your cards: {your_card}, current score: {your_sum}")
        print(f"   Computer's first card: {com_card[0]}")

        if your_sum == 21:
            end_game = True

        get_another_card = input(
            "Type 'y' to get another card, type 'n' to pass: ")

        if get_another_card == 'y':
            your_card.append(get_more_card())
            your_sum = sum(your_sum, your_card[-1])

            if your_sum > 21:
                end_game = True

        elif get_another_card == 'n':
            end_game = True

    print(f"   Your final hand: {your_card}, final score: {your_sum}")
    print(f"   Computer's final hand: {com_card}, final score: {com_sum}")

    if your_sum > com_sum and your_sum <= 21:
        print("You win :)")
    else:
        print("You Lose :(")

    wanna_play = input(
        "Do you want to play a game of Blackjack? Type 'y' or 'n': ")
    if wanna_play == 'y':
        clear()
    elif wanna_play == 'n':
        start_game = False
