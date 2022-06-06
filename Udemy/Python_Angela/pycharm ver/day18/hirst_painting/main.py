import turtle
import random

turtle.colormode(255)
t = turtle.Turtle()
t.speed("fastest")
t.penup()
t.hideturtle()
color_list = color_list = [(246, 241, 231), (226, 235, 242), (246, 234, 239), (233, 244, 238), (201, 161, 106), (146, 79, 62), (51, 101, 132), (135, 169, 187), (231, 213, 105), (192, 141, 158), (29, 40, 52), (138, 71, 86), (145, 176, 154), (162, 149, 65), (196, 95, 76), (71, 49, 37), (58, 114, 97), (33, 46, 39), (63, 149, 172), (219, 176, 187), (188, 96, 120), (103, 147, 110), (224, 178, 170), (27, 82, 74), (95, 47, 40), (45, 61, 98), (96, 47, 59), (22, 82, 91), (173, 202, 181), (178, 190, 209)]

t.setheading(225)
t.forward(300)
t.setheading(0)
number_of_dots = 100

for dot_count in range(1, number_of_dots + 1):
    t.dot(20, random.choice(color_list))
    t.forward(50)

    if dot_count % 10 == 0:
        t.setheading(90)
        t.forward(50)
        t.setheading(180)
        t.forward(500)
        t.setheading(0)


screen = turtle.Screen()
screen.exitonclick()