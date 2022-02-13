# Dictionaries, Nesting, Build-Auction

from lib.auction import logo
from replit import clear
programming_dictionary = {
    "Bug": "An error in a program that prevents the program from running as expected.",
    "Function": "A piece of code that you can easily call over and over again.",
}

# print(programming_dictionary["Bug"])

programming_dictionary["Loop"] = "The action of doing something over and over again."

# Create an empty dictionary.
empty_dictionary = {}

# Wipe an existing dictionary.
# programming_dictionary = {}

# Edit an item in a dictionary
programming_dictionary["Bug"] = "A moth in your computer."
print(programming_dictionary)

for key in programming_dictionary:
    print(key)
    print(programming_dictionary[key])
#
student_scores = {
    "Harry": 81,
    "Ron": 78,
    "Hermione": 99,
    "Draco": 74,
    "Neville": 62,
}
# 🚨 Don't change the code above 👆

# TODO-1: Create an empty dictionary called student_grades.
student_grades = {}


# TODO-2: Write your code below to add the grades to student_grades.👇
for name in student_scores:
    score = student_scores[name]
    if score > 90 and score <= 100:
        student_grades[name] = "Outstanding"
    elif score > 80 and score <= 90:
        student_grades[name] = "Exceeds Expectations"
    elif score > 70 and score <= 80:
        student_grades[name] = "Acceptable"
    else:
        student_grades[name] = "Fail"


# 🚨 Don't change the code below 👇
print(student_grades)
#

# Nesting
capitals = {
    "France": "Paris",
    "Germany": "Berlin",
}

# Nesting a List in a Dictionary

travel_log = {
    "France": ["Paris", "Lille", "Dijon"],
    "Germany": ["Berlin", "Hamburg", "Stuttgart"],
}

# Nesting Dictionary in a Dictionary

travel_log = {
    "France": {"cities_visited": ["Paris", "Lille", "Dijon"], "total_visits": 12},
    "Germany": {"cities_visited": ["Berlin", "Hamburg", "Stuttgart"], "total_visits": 5},
}

# Nesting Dictionaries in Lists

travel_log = [
    {
        "country": "France",
        "cities_visited": ["Paris", "Lille", "Dijon"],
        "total_visits": 12,
    },
    {
        "country": "Germany",
        "cities_visited": ["Berlin", "Hamburg", "Stuttgart"],
        "total_visits": 5,
    },
]
#
travel_log = [
    {
        "country": "France",
        "visits": 12,
        "cities": ["Paris", "Lille", "Dijon"]
    },
    {
        "country": "Germany",
        "visits": 5,
        "cities": ["Berlin", "Hamburg", "Stuttgart"]
    },
]
# 🚨 Do NOT change the code above

# TODO: Write the function that will allow new countries
# to be added to the travel_log. 👇


def add_new_country(country, visits, cities):
    new_country = {}
    new_country["country"] = country
    new_country["visits"] = visits
    new_country["cities"] = cities
    travel_log.append(new_country)
    # travel_log.append({
    #   "country":country,
    #   "visits":visits,
    #   "cities":cities
    #   })


# 🚨 Do not change the code below
add_new_country("Russia", 2, ["Moscow", "Saint Petersburg"])
print(travel_log)
#
# HINT: You can call clear() to clear the output in the console.
print(logo)
print("Welcome to the secret auction program.")

auction = {}
is_ING = True

while is_ING:
    name = input("What is your name?: ")
    bid = int(input("What's your bid?: $"))

    auction[name] = bid
    ING = input("Are there any other bidders? Type 'yes' or 'no'.\n").lower()
    if ING == "yes":
        clear()
    else:
        is_ING = False

# max_bidder = 0
# successful_bidder = ""
# for name, val in auction.items():
#   if max_bidder < val:
#     max_bidder = val
#     successful_bidder = name


def find_highest_bidder(bidding_record):
    highest_bid = 0
    winner = ""

    for bidder in bidding_record:
        bid_amount = bidding_record[bidder]
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = bidder

    print(f"The winner is {winner} with a bid of ${highest_bid}.")


find_highest_bidder(auction)
