import pandas as pd
import numpy as np

df1 = winemag_pd[["region_1", "price", "variety"]].rename(
    columns={"region_1": "region"}
)
df2 = winemag_pd[["region_2", "price", "variety"]].rename(
    columns={"region_2": "region"}
)
df = pd.merge(df1, df2, how="outer", on=["region", "price", "variety"])
df_clean = df.dropna()

df_clean["expensive_rank"] = df_clean.groupby("region")["price"].rank(
    method="dense", ascending=False
)
df_clean["cheap_rank"] = df_clean.groupby("region")["price"].rank(
    method="dense", ascending=True
)
df_cheap = df_clean[["region", "variety", "cheap_rank"]]
df_expensive = df_clean[["region", "variety", "expensive_rank"]]
df_cheap = df_cheap[df_cheap["cheap_rank"] == 1]
df_expensive = df_expensive[df_expensive["expensive_rank"] == 1]
merged = pd.merge(df_cheap, df_expensive, on="region", how="outer")
merged = (
    merged.rename(
        columns={
            "variety_x": "cheapest_variety",
            "variety_y": "most_expensive_variety",
        }
    )
    .sort_values(by="region")
    .reset_index()
)
result = merged[["region", "cheapest_variety", "most_expensive_variety"]]
