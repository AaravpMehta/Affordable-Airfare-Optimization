import pandas as pd

q1 = pd.read_csv("data/processed/db1b/JFK_LAX_DB1B_Q1_2025.csv")
q2 = pd.read_csv("data/processed/db1b/JFK_LAX_DB1B_Q2_2025.csv")

print("Q1 shape:", q1.shape)
print("Q2 shape:", q2.shape)

print("\nQ1 columns:")
print(q1.columns.tolist())

print("\nQ2 columns:")
print(q2.columns.tolist())

print("\nQ1 first five rows:")
print(q1.head())

print("\nQ2 first five rows:")
print(q2.head())

print("\nQ1 column names:")
for col in q1.columns:
    print(col)

print("\nQ2 column names:")
for col in q2.columns:
    print(col)

print("\nQ1 market coupons:")
print(q1["MARKET_COUPONS"].value_counts().sort_index())

print("\nQ2 market coupons:")
print(q2["MARKET_COUPONS"].value_counts().sort_index())

print("\nQ1 origin-destination pairs:")
print(q1.groupby(["ORIGIN", "DEST"]).size().head(10))

print("\nQ2 origin-destination pairs:")
print(q2.groupby(["ORIGIN", "DEST"]).size().head(10))

q1_nonstop = q1[q1["MARKET_COUPONS"] == 1]
q2_nonstop = q2[q2["MARKET_COUPONS"] == 1]

print("\nQ1 nonstop records:", len(q1_nonstop))
print("Q2 nonstop records:", len(q2_nonstop))

print("\nQ1 nonstop passenger count:",
      q1_nonstop["PASSENGERS"].sum())

print("Q2 nonstop passenger count:",
      q2_nonstop["PASSENGERS"].sum())

print("\nQ1 nonstop fare statistics:")
print(q1_nonstop["MARKET_FARE"].describe(
    percentiles=[0.25, 0.50, 0.75, 0.90]
))

print("\nQ2 nonstop fare statistics:")
print(q2_nonstop["MARKET_FARE"].describe(
    percentiles=[0.25, 0.50, 0.75, 0.90]
))

print("\nQ1 zero or negative fares:",
      (q1_nonstop["MARKET_FARE"] <= 0).sum())

print("Q2 zero or negative fares:",
      (q2_nonstop["MARKET_FARE"] <= 0).sum())

print("\nQ1 fares above $2000:",
      (q1_nonstop["MARKET_FARE"] > 2000).sum())

print("Q2 fares above $2000:",
      (q2_nonstop["MARKET_FARE"] > 2000).sum())

q1_valid = q1_nonstop[q1_nonstop["MARKET_FARE"] > 0]
q2_valid = q2_nonstop[q2_nonstop["MARKET_FARE"] > 0]

print("\nQ1 valid-fare quartiles:")
print(q1_valid["MARKET_FARE"].quantile([0.25, 0.50, 0.75]))

print("\nQ2 valid-fare quartiles:")
print(q2_valid["MARKET_FARE"].quantile([0.25, 0.50, 0.75]))