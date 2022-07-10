from tkinter import *

window = Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)
window.config(padx=110, pady=220)

# Label

my_label = Label(text="I Am a Label", font=("Arial", 24, "italic"))
# my_label.pack(side="left")
# my_label.pack(expand=True)
my_label.pack()

my_label["text"] = "New Text"
my_label.config(text="New Text")
# my_label.place(x=0, y=0)
my_label.grid(column=0, row=0)
my_label.config(padx=50, pady=50)


def button_clicked():
    print("clicked")
    my_label.config(text=input.get())


button = Button(text="Click Me", command=button_clicked)
# button.pack()
button.grid(column=1, row=1)

new_button = Button(text="New Button")
new_button.grid(column=2, row=0)

# Entry
input = Entry(width=10)
# input.pack()
print(input.get())
input.grid(column=3, row=2)

window.mainloop()
# https://docs.python.org/3/library/tkinter.html
# https://tcl.tk/man/tcl8.6/TkCmd/pack.htm
