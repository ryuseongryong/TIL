from turtle import Turtle, Screen

screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")
colors = ["red", "orange", "yellow", "green", "blue", "purple"]

for turtle_idx in range(0, len(colors)):
    t = Turtle(shape="turtle")
    t.color(colors[turtle_idx])
    t.penup()
    t.goto(x=-230, y= -70 + turtle_idx * 30)



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