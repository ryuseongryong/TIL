import pandas as pd

df = pd.read_csv("salaries_by_college_major.csv")
df.head()

df.shape
df.columns
df.isna()
df.tail()

clean_df = df.dropna()
clean_df.tail()
