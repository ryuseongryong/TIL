# Default value Arguments
def foo(a, b=2, c=3):
    print(a, b, c)


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

# Unlimited Keyword Arguments
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


class Car:
    def __init__(self, **kw):
        # self.make = kw["make"]
        # self.model = kw["model"]
        self.make = kw.get("make")
        self.model = kw.get("model")


my_car = Car(make="Hyundai")
print(my_car.model)
