from tkinter import *

# import os

# os.chdir("./Udemy/Python_Angela/second_local/day28/pomodoro-start/")
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
window.config(padx=20, pady=10, bg=YELLOW)

canvas = Canvas(width=413, height=531, bg=YELLOW, highlightthickness=0)
bg_img = PhotoImage(file="image.png")
canvas.create_image(206, 265, image=bg_img)
canvas.create_text(206, 385, text="00:00", fill="black", font=(FONT_NAME, 35, "bold"))
canvas.pack()

window.mainloop()
