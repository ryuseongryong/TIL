import random
from turtle import Turtle, Screen

screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color(red/orange/yellow/green/blue/purple): ")
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
in_race_on = False
all_turtles = []

for turtle_idx in range(0, len(colors)):
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[turtle_idx])
    new_turtle.penup()
    new_turtle.goto(x=-230, y= -70 + turtle_idx * 30)
    all_turtles.append(new_turtle)


if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"You've won! The {winning_color} turtle is the winner!")
            else:
                print(f"You've lose! The {winning_color} turtle is the winner!")
        rand_distance = random.randint(0, 10)
        turtle.forward(rand_distance)

screen.exitonclick()

# def move_forwards():
#     t.forward(10)

# def move_backwards():
#     t.backward(10)

# def turn_left():
#     new_heading = t.heading() + 10
#     t.setheading(new_heading)

# def turn_right():
#     new_heading = t.heading() - 10
#     t.setheading(new_heading)

# def clear():
#     t.clear()
#     t.penup()
#     t.home()
#     t.pendown()



# screen.listen()
# screen.onkey(move_forwards, 'w')
# screen.onkey(move_backwards, 's')
# screen.onkey(turn_left, 'a')
# screen.onkey(turn_right, 'd')
# screen.onkey(clear, 'c')