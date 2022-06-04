from turtle import Turtle, Screen
import random
import turtle
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
turtle.colormode(255)
# t.fillcolor(255)
# t.left(180)

def random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r, g, b)
        return color


# colors = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
# directions = [0, 90, 180, 270]
# t.pensize(10)
t.speed("fastest")

# def draw_shape(sides):
#     angle = 360 / sides
#     for _ in range(sides):
#         t.forward(100)
#         t.right(angle)

# for shape in range(3, 11):
#     t.color(random.choice(colors))
#     draw_shape(shape)

# for _ in range(100):
#     # t.color(random.choice(colors))
#     t.color(random_color())
#     t.forward(30)
#     t.setheading(random.choice(directions))
# for _ in range(359):
#     cur_heading = t.heading()
#     t.setheading(cur_heading + 1)
#     t.color(random_color())
#     t.circle(100)

def draw_spirograph(size_of_gap):
    for _ in range(int(360 / size_of_gap)):
        t.color(random_color())
        t.circle(100)
        t.setheading(t.heading() + size_of_gap)

draw_spirograph(5)








screen = Screen()
screen.exitonclick()