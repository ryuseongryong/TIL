# # First
# import random

# names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]

# # student_score = {new_key: new_value for item in names}
# # passed_students = {new_key:new_value for (key, value) in dictionary.items()}


# student_score = {student: random.randint(1, 100) for student in names}
# print(student_score)

# passed_students = {
#     student: score for (student, score) in student_score.items() if score >= 60
# }
# print(passed_students)

# # Second
# sentence = "What is the Airspeed Velocity of an Unladen Swallow?"

# result = {word: len(word) for word in sentence.split(" ")}
# print(result)

# # Third
# weather_c = {
#     "Monday": 12,
#     "Tuesday": 14,
#     "Wednesday": 15,
#     "Thursday": 14,
#     "Friday": 21,
#     "Saturday": 22,
#     "Sunday": 24,
# }
# weather_f = {day: (temp_c * 9 / 5) + 32 for (day, temp_c) in weather_c.items()}

# print(weather_f)
