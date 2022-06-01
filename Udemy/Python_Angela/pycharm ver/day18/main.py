from turtle import Turtle, Screen

timmy_the_turtle = Turtle()
# timmy_the_turtle.shape("turtle")
# timmy_the_turtle.color("red")
# timmy_the_turtle.forward(100)
# timmy_the_turtle.right(90)

for _ in range(4):
    timmy_the_turtle.left(90)
    for i in range(10):
        timmy_the_turtle.dot()
        timmy_the_turtle.penup()
        timmy_the_turtle.forward(10)

screen = Screen()
screen.exitonclick()
