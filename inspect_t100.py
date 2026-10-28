import pandas as pd

file_path = "data/processed/t100/JFK_LAX_T100_2025.csv"

df = pd.read_csv(file_path)

print("First five rows:")
print(df.head())

print("\nRows by CLASS:")
print(df["CLASS"].value_counts())

scheduled = df[df["CLASS"] == "F"]

jan_jun = scheduled[scheduled["MONTH"] <= 6]

print("\nJFK-LAX scheduled service, January-June 2025:")
print(jan_jun)

print("\nNumber of records:", len(jan_jun))

print("\nTotal passengers by month:")
print(jan_jun.groupby("MONTH")["PASSENGERS"].sum())

print("\nAvailable columns:")
print(df.columns.tolist())

print("\nPassengers by airline, January–June:")
print(
    jan_jun.groupby("UNIQUE_CARRIER_NAME")["PASSENGERS"]
    .sum()
    .sort_values(ascending=False)
)