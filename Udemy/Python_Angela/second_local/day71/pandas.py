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

# 특정 열에 접근2
print(clean_df["Mid-Career Median Salary"].max())
print(
    f"Index for the max mid career salary: {clean_df['Mid-Career Median Salary'].idxmax()}"
)
clean_df["Undergraduate Major"][8]

print(clean_df["Starting Median Salary"].min())
clean_df["Undergraduate Major"].loc[clean_df["Starting Median Salary"].idxmin()]

clean_df.loc[clean_df["Mid-Career Median Salary"].idxmin()]

(
    clean_df["Mid-Career 90th Percentile Salary"]
    - clean_df["Mid-Career 10th Percentile Salary"]
)

clean_df["Mid-Career 90th Percentile Salary"].subtract(
    clean_df["Mid-Career 10th Percentile Salary"]
)

spread_col = (
    clean_df["Mid-Career 90th Percentile Salary"]
    - clean_df["Mid-Career 10th Percentile Salary"]
)

clean_df.insert(1, "Spread", spread_col)
clean_df.head()

low_risk = clean_df.sort_values("Spread")
low_risk[["Undergraduate Major", "Spread"]].head()

highest_potential = clean_df.sort_values(
    "Mid-Career 90th Percentile Salary", ascending=False
)
highest_potential[["Undergraduate Major", "Mid-Career 90th Percentile Salary"]].head()

highest_spread = clean_df.sort_values("Spread", ascending=False)
highest_spread[["Undergraduate Major", "Spread"]].head()
