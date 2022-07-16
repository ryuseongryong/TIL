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
reps = 0

# ---------------------------- TIMER RESET ------------------------------- #

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED, bg=YELLOW)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK, bg=YELLOW)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN, bg=YELLOW)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = count // 60
    count_sec = count % 60
    if count_min < 10:
        count_min = f"0{count_min}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        window.after(1000, count_down, count - 1)
    else:
        start_timer()


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
