# coding: utf-8
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

totals=pd.read_csv('totals.csv',names=['totals'])
totals=totals[totals['totals']>0]
bins=np.arange(120,320,1)
totals.plot.hist(alpha=1,bins=bins)
plt.show()
