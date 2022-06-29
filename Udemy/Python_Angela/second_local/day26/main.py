number = [1, 2, 3]
new = [n + 1 for n in number]

name = "ryuseongryong"
letters = [letter for letter in name]

# print(number)
# print(new)
print(letters)

range_num = [n * 2 for n in range(1, 5)]
print(range_num)

names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]
short_names = [name for name in names if len(name) < 5]

print(names)
print(short_names)

cap_names = [name.upper() for name in names if len(name) > 4]
print(cap_names)
