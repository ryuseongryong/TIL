from turtle import Turtle, Screen
import random
# import heroes

timmy_the_turtle = Turtle()
# timmy_the_turtle.shape("turtle")
# timmy_the_turtle.color("red")
# timmy_the_turtle.forward(100)
# timmy_the_turtle.right(90)

# for _ in range(4):
#     timmy_the_turtle.left(90)
#     for i in range(10):
#         timmy_the_turtle.dot()
#         timmy_the_turtle.penup()
#         timmy_the_turtle.forward(10)

# print(heroes.gen())

t = Turtle()
t.left(180)

colors = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]

def draw_shape(sides):
    angle = 360 / sides
    for _ in range(sides):
        t.forward(100)
        t.right(angle)

for shape in range(3, 11):
    t.color(random.choice(colors))
    draw_shape(shape)







screen = Screen()
screen.exitonclick()