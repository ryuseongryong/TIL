# functions, code blocks, while Loop, Indentation

def my_function():
    print("Hello")
    print("Bye")


my_function()

# Defining Functions


def function_name():
    # Do This
    # Then do this
    # Finally do this
    print()


# Calling Functions
function_name()

# Robot world
# def turn_around():
#     turn_left()
#     turn_left()

# def move_two():
#     move()
#     move()

# def turn_right():
#     turn_left()
#     turn_left()
#     turn_left()

# def turn_circle():
#     turn_left()
#     turn_left()
#     turn_left()
#     turn_left()

# def move_around():
#     turn_left()
#     move()
#     turn_right()
#     move()
#     turn_right()
#     move()
#     turn_right()
#     move()
#     turn_right()

# move_around()

# Robot World2
# def turn_right():
#     turn_left()
#     turn_left()
#     turn_left()

# def jump_hurdle():
#     move()
#     turn_left()
#     move()
#     turn_right()
#     move()
#     turn_right()
#     move()
#     turn_left()

# for hurdle in range(0, 6):
#     jump_hurdle()

# Indentation
# Four Spaces are standard in Python
# anyway code editor like PEP 8 etc, make one tap to four spaces.

# while

# about for
# for item in list_of_items:
# Do something to each item

# for number in range(a, b):
# print(number)

# about while
# while something_is_true:
# Do something repeatedly

# Robot World3
# def turn_right():
#     turn_left()
#     turn_left()
#     turn_left()

# def jump():
#     turn_left()
#     move()
#     turn_right()
#     move()
#     turn_right()
#     move()
#     turn_left()

# while not at_goal():
#     while front_is_clear():
#         move()
#     while wall_in_front():
#         jump()

# Robot World 4
# def turn_right():
#     turn_left()
#     turn_left()
#     turn_left()

# def jump():
#     turn_left()
#     while wall_on_right() and front_is_clear():
#         move()
#         if at_goal():
#             break
#     while right_is_clear():
#         turn_right()
#         move()
#         if at_goal():
#             break
# while not at_goal():
#     while front_is_clear():
#         move()
#     while wall_in_front():
#         jump()
#
# Maze ver1.
# def turn_right():
#     turn_left()
#     turn_left()
#     turn_left()

# while not at_goal():
#     while front_is_clear():
#         if at_goal():
#             break
#         if wall_on_right():
#             move()
#         elif right_is_clear():
#             turn_right()
#             move()
#     while wall_in_front():
#         if at_goal():
#             break
#         if wall_on_right():
#             turn_left()
#         elif right_is_clear():
#             turn_right()
#             move()
# Maze ver2.
# def turn_right():
#     turn_left()
#     turn_left()
#     turn_left()

# while front_is_clear():
#     move()
# turn_left()

# while not at_goal():
#     if right_is_clear():
#         turn_right()
#         move()
#     elif front_is_clear():
#         move()
#     else:
#         turn_left()
