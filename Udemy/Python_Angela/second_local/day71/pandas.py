import pandas as pd

df = pd.read_csv("salaries_by_college_major.csv")
df.head()

# 행 수 확인
df.shape

# 행 열 수 확인
df.columns

# 검사
df.isna()

# 마지막 5행 확인
df.tail()

# 마지막 줄 삭제
clean_df = df.dropna()
clean_df.tail()

# 특정 열에 접근
clean_df["Starting Median Salary"]
clean_df["Starting Median Salary"].max
clean_df["Starting Median Salary"].idxmax()
clean_df["Undergraduate Major"].loc[43]
clean_df["Undergraduate Major"][43]
clean_df.loc[43]
