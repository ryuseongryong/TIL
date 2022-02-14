# Function, Function with Inputs, Function with Outputs, Docstring

# Fucntion with Outputs

def format_name(f_name, l_name):
    new_f_name = ""
    new_l_name = ""
    for num in range(len(f_name)):
        if num == 0:
            new_f_name = f_name[num].upper()
        else:
            new_f_name += f_name[num].lower()

    for num in range(len(l_name)):
        if num == 0:
            new_l_name = l_name[num].upper()
        else:
            new_l_name += l_name[num].lower()

    return new_f_name + new_l_name


first = input("firstname: ")
last = input("lastname: ")
print(format_name(first, last))

# => title function make these as same!


def format_name2(f_name, l_name):
    formated_f_name = f_name.title()
    formated_l_name = l_name.title()
    return f"{formated_f_name} {formated_l_name}"


formated_string = format_name("SEONGRYONG", "ryu")
print(formated_string)

# Fucntion with Outputs2


def format_name(f_name, l_name):
    if f_name == "" or l_name == "":
        return "You didn't provide valid inputs."

    formated_f_name = f_name.title()
    formated_l_name = l_name.title()
    return f"Result: {formated_f_name} {formated_l_name}"


print(format_name(input("What is your first name? "),
      input("What is your last name? ")))
#


def is_leap(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def days_in_month(year, month):
    if month > 12 or month < 1:
        return "Invalid Month!"
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    leap_year_Feb = 29
    if is_leap(year) and month == 2:
        return leap_year_Feb
    else:
        return month_days[month - 1]


# 🚨 Do NOT change any of the code below
year = int(input("Enter a year: "))
month = int(input("Enter a month: "))
days = days_in_month(year, month)
print(days)
