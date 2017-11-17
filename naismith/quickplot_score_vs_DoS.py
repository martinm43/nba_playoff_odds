# coding: utf-8
import pandas as pd
games=pd.read_csv('results.csv',names=['id','score','dDoS'])
import matplotlib.pyplot as plt
plt.plot(games['dDoS'],games['score'],'o')
plt.show()
