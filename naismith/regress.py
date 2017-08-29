# coding: utf-8
import pandas as pd
import statsmodels.api as sm
import numpy as np
get_ipython().magic(u'ls')
df = pd.read_csv("burke_results.csv",names=["score","diff"])
df
pd.describe()
df.describe()
df['away_win'] = df['score']>0
df
