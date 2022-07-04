student_dict = {"student": ["Angela", "James", "Lily"], "score": [56, 76, 98]}

# Looping through dictionaries
for (key, value) in student_dict.items():
    print(key)
    print(value)

import pandas

student_df = pandas.DataFrame(student_dict)
print(student_df)

# Loop through a data frame
# for (key, value) in student_df.items():
#     print(key)
#     print(value)

# Loop through rows of a data frame
for (index, row) in student_df.iterrows():
    # print(index)
    # print(row.student)
    if row.student == "Lily":
        print(row.score)
