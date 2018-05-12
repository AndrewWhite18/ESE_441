#this script interpolates the scaled sentiment data

import pandas as pd


df = pd.read_csv("../scaled_2.csv", parse_dates=["tweet_date"])
df.set_index('tweet_date', inplace=True)
all_days = pd.date_range(df.index.min(), df.index.max(), freq='D')
dfr = df.reindex(index=all_days)

new_df = dfr.interpolate(method='time')

new_df.to_csv('scaled_interpolated2.csv')