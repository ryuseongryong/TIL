import os

os.chdir("./Udemy/Python_Angela/second_local/day26")
# first
# number = [1, 2, 3]
# new = [n + 1 for n in number]

# name = "ryuseongryong"
# letters = [letter for letter in name]

# # print(number)
# # print(new)
# print(letters)

# range_num = [n * 2 for n in range(1, 5)]
# print(range_num)

# names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]
# short_names = [name for name in names if len(name) < 5]

# print(names)
# print(short_names)

# cap_names = [name.upper() for name in names if len(name) > 4]
# print(cap_names)

# second
# numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

# squared_numbers = [n**2 for n in numbers]

# print(squared_numbers)

# third
# numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

# result = [n for n in numbers if n % 2 == 0]

# print(result)

# forth
with open("file1.txt") as f1:
    nums = f1.read()
    nums = nums.splitlines()
    nums = [int(n) for n in nums]
    nums.sort()
    f1_nums = nums
with open("file2.txt") as f2:
    nums = f2.read()
    nums = nums.splitlines()
    nums = [int(n) for n in nums]
    nums.sort()
    f2_nums = nums

print(f1_nums)
print(f2_nums)

result = [n for n in f1_nums if n in f2_nums]
print(result)
# ---
# forth-ref
with open("file1.txt") as file1:
    file_1_data = file1.readlines()
with open("file2.txt") as file2:
    file_2_data = file2.readlines()

result = [int(num) for num in file_1_data if num in file_2_data]
