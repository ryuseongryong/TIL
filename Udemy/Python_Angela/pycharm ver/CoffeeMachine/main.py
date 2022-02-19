MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}


# TODO :  print report

# TODO :  check resources sufficient

# TODO :  process coins

# TODO :  check transaction successful

# TODO :  make coffee

# Todo: 1. Prompt user by asking “What would you like? (espresso/latte/cappuccino):”
# Todo: a. Check the user’s input to decide what to do next.
# Todo: b. The prompt should show every time action has completed, e.g. once the drink is
# Todo: dispensed. The prompt should show again to serve the next customer.
# Todo: 2. Turn off the Coffee Machine by entering “off” to the prompt.
# Todo: a. For maintainers of the coffee machine, they can use “off” as the secret word to turn off the machine. Your code should end execution when this happens.
# Todo: 3. Print report.
# Todo: a. When the user enters “report” to the prompt, a report should be generated that shows
# Todo: the current resource values. e.g.
# Todo: Water: 100ml
# Todo: Milk: 50ml
# Todo: Coffee: 76g
# Todo: Money: $2.5
# Todo: 4. Check resources sufficient?
# Todo: a. When the user chooses a drink, the program should check if there are enough
# Todo: resources to make that drink.
# Todo: b. E.g. if Latte requires 200ml water but there is only 100ml left in the machine. It should
# Todo: not continue to make the drink but print: “Sorry there is not enough water.”
# Todo: c. The same should happen if another resource is depleted, e.g. milk or coffee.
# Todo: 5. Process coins.
# Todo: a. If there are sufficient resources to make the drink selected, then the program should
# Todo: prompt the user to insert coins.
# Todo: b. Remember that quarters = $0.25, dimes = $0.10, nickles = $0.05, pennies = $0.01
# Todo: c. Calculate the monetary value of the coins inserted. E.g. 1 quarter, 2 dimes, 1 nickel, 2
# Todo: pennies = 0.25 + 0.1 x 2 + 0.05 + 0.01 x 2 = $0.52
# Todo: 6. Check transaction successful?
# Todo: a. Check that the user has inserted enough money to purchase the drink they selected.
# Todo: E.g Latte cost $2.50, but they only inserted $0.52 then after counting the coins the
# Todo: program should say “Sorry that's not enough money. Money refunded.”.
# Todo: b. But if the user has inserted enough money, then the cost of the drink gets added to the
# Todo: machine as the profit and this will be reflected the next time “report” is triggered. E.g.
# Todo: Water: 100ml
# Todo: Milk: 50ml
# Todo: Coffee: 76g
# Todo: Money: $2.5
# Todo: c. If the user has inserted too much money, the machine should offer change.
# Todo: E.g. “Here is $2.45 dollars in change.” The change should be rounded to 2 decimal
# Todo: places.
# Todo: 7. Make Coffee.
# Todo: a. If the transaction is successful and there are enough resources to make the drink the
# Todo: user selected, then the ingredients to make the drink should be deducted from the
# Todo: coffee machine resources.
# Todo: E.g. report before purchasing latte:
# Todo: Water: 300ml
# Todo: Milk: 200ml
# Todo: Coffee: 100g
# Todo: Money: $0
# Todo: Report after purchasing latte:
# Todo: Water: 100ml
# Todo: Milk: 50ml
# Todo: Coffee: 76g
# Todo: Money: $2.5
# Todo: b. Once all resources have been deducted, tell the user “Here is your latte. Enjoy!”. If
# Todo: latte was their choice of drink.