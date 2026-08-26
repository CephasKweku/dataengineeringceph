import sys
import pandas as pd

print("arguments", sys.argv)

month = int(sys.argv[1])

df = pd.DataFrame({"day": [1, 2], "number_passangers": [3, 4]})
print(df.head())

df.to_parquet(f"output_{month}.parquet")

print(f"Running pipeline for month {month}")