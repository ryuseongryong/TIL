# import tkinter

# window = tkinter.Tk()
# window.title("My First GUI Program")
# window.minsize(width=500, height=300)

# # Label

# my_label = tkinter.Label(text="I Am a Label", font=("Arial", 24, "italic"))
# # my_label.pack(side="left")
# my_label.pack(expand=True)


# import turtle

# t = turtle.Turtle()
# t.write("hello")

# window.mainloop()
# # https://docs.python.org/3/library/tkinter.html
# # https://tcl.tk/man/tcl8.6/TkCmd/pack.htm

# Default value Arguments
# def foo(a, b=2, c=3):
#     print(a, b, c)


# Unlimited positional Arguments
def add(*args):
    # type of args = tuple
    print(args)
    print(args[0])

    sum = 0
    for n in args:
        sum += n
    return sum


print(add(1, 2, 3))


def calculate(n, **kwargs):
    # type of kwargs = dict
    print(kwargs)
    # for key, val in kwargs.items():
    #     print(key)
    #     print(val)
    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)


calculate(2, add=3, multiply=5)
