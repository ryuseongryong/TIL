from tkinter import *
import os

os.chdir("./Udemy/Python_Angela/second_local/day28/pomodoro-start/")
# print(os.getcwd())

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- TIMER RESET ------------------------------- #

# ---------------------------- TIMER MECHANISM ------------------------------- #

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
canvas = Canvas(width=413, height=531)
bg_img = PhotoImage(file="toamto.png")
canvas.create_image(206, 265, image=bg_img)
canvas.pack()

window.mainloop()
