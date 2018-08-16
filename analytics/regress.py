# coding: utf-8
get_ipython().magic(u'load regress.py')
# %load regress.py
import pandas as pd
import statsmodels.api as sm
import numpy as np
get_ipython().magic(u'ls')
df = pd.read_csv("burke_results.csv",names=["score","diff"])
df.describe()
df['away_win'] = df['score']>0
df
fullset=df[['diff','away_win']]
fullset
logit=sm.Logit(fullset['away_win'], fullset[['diff']])
result=logit.fit()
print result.summary()
get_ipython().magic(u'save regress 1-15')
