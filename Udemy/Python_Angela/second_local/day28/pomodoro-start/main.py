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
def start_timer():
    count_down(5 * 60)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = count // 60
    count_sec = count % 60

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        window.after(1000, count_down, count - 1)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
window.config(padx=20, pady=20, bg=YELLOW)


title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=413, height=531, bg=YELLOW, highlightthickness=0)
bg_img = PhotoImage(file="image.png")
canvas.create_image(206, 265, image=bg_img)
timer_text = canvas.create_text(
    206, 385, text="00:00", fill="black", font=(FONT_NAME, 35, "bold")
)
canvas.grid(column=1, row=1)


start_button = Button(
    text="Start",
    bg=YELLOW,
    highlightthickness=0,
    highlightbackground=YELLOW,
    command=start_timer,
)
start_button.grid(column=0, row=2)
reset_button = Button(
    text="Reset", bg=YELLOW, highlightthickness=0, highlightbackground=YELLOW
)
reset_button.grid(column=2, row=2)

check_marker = Label(text="✓", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
check_marker.grid(column=1, row=2)

window.mainloop()
