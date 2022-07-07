import tkinter

window = tkinter.Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)

# Label

my_label = tkinter.Label(text="I Am a Label", font=("Arial", 24, "italic"))
# my_label.pack(side="left")
my_label.pack(expand=True)


import turtle

t = turtle.Turtle()
t.write("hello")

window.mainloop()
# https://docs.python.org/3/library/tkinter.html
# https://tcl.tk/man/tcl8.6/TkCmd/pack.htm
