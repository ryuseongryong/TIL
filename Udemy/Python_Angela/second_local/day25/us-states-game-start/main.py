import turtle, os

print(os.getcwd())
os.chdir("./Udemy/Python_Angela/second_local/day25/us-states-game-start")

screen = turtle.Screen()
screen.title("U.S. States Game")
screen.addshape("blank_states_img.gif")
turtle.shape("blank_states_img.gif")

answer_state = screen.textinput(
    title="Guess the State", prompt="What is another state's name?"
)
print(answer_state)

screen.exitonclick()
