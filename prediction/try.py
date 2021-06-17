import pandas as pd

data = pd.read_feather("data/examination/Audiometry.feather")

data.columns.to_series().to_csv("columns.txt", header=None, index=None, sep=' ', mode='a')