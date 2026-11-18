"""
Project: Cleaning & Analysing Online Store Orders (sample practice project)
Goal: take a messy orders file, clean it step by step, then answer
simple business questions with numbers and charts.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- 1) Load the raw file ----------
df = pd.read_csv("raw_orders.csv")
print("Rows before cleaning:", len(df))

# ---------- 2) Clean ----------
df = df.drop_duplicates()                                  # same order repeated
df["city"] = df["city"].str.strip().str.title()            # ' cairo ' -> 'Cairo'
df["city"] = df["city"].fillna("Unknown")                  # missing city
df["price"] = df["price"].str.replace(" EGP", "", regex=False).astype(float)
df["order_date"] = pd.to_datetime(df["order_date"])
df = df[~(df["quantity"] < 0)]                             # impossible quantity
df["quantity"] = df["quantity"].fillna(df["quantity"].median())
df["rating"] = df["rating"].fillna(df["rating"].median())
df["revenue"] = df["quantity"] * df["price"]
df["month"] = df["order_date"].dt.month
print("Rows after cleaning:", len(df))

# ---------- 3) Analyse ----------
total = df["revenue"].sum()
by_prod = df.groupby("product")["revenue"].sum().sort_values(ascending=False)
by_city = df.groupby("city")["revenue"].sum().sort_values(ascending=False)
by_month = df.groupby("month")["revenue"].sum()
by_seg = df.groupby("segment").agg(orders=("order_id", "count"),
                                   revenue=("revenue", "sum"),
                                   avg_order=("revenue", "mean"),
                                   avg_rating=("rating", "mean"))
print("Total revenue:", round(total))
print(by_prod.head(3)); print(by_city); print(by_seg.round(1))

# ---------- 4) Charts ----------
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(6, 3.4))
by_prod.sort_values().plot.barh(ax=ax, color="#2E75B6")
ax.set_title("Revenue by product (EGP)"); ax.set_ylabel("")
plt.tight_layout(); plt.savefig("py_chart_products.png", dpi=170); plt.close()

fig, ax = plt.subplots(figsize=(6, 3.4))
by_month.plot(ax=ax, marker="o", color="#C55A11")
ax.set_title("Revenue by month (EGP)"); ax.set_xlabel("Month"); ax.set_xticks(range(1, 13))
plt.tight_layout(); plt.savefig("py_chart_months.png", dpi=170); plt.close()

fig, ax = plt.subplots(figsize=(6, 3.4))
by_seg["avg_order"].plot.bar(ax=ax, color=["#70AD47", "#2E75B6", "#FFC000"], rot=0)
ax.set_title("Average order value by customer type (EGP)"); ax.set_xlabel("")
plt.tight_layout(); plt.savefig("py_chart_segments.png", dpi=170); plt.close()

df.to_csv("clean_orders.csv", index=False)
