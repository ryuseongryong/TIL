from tkinter import *

window = Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)

# Label

my_label = Label(text="I Am a Label", font=("Arial", 24, "italic"))
# my_label.pack(side="left")
# my_label.pack(expand=True)
my_label.pack()

my_label["text"] = "New Text"
my_label.config(text="New Text")


def button_clicked():
    print("clicked")
    my_label.config(text=input.get())


button = Button(text="Click Me", command=button_clicked)
button.pack()

# Entry
input = Entry(width=10)
input.pack()
print(input.get())


window.mainloop()
# https://docs.python.org/3/library/tkinter.html
# https://tcl.tk/man/tcl8.6/TkCmd/pack.htm
