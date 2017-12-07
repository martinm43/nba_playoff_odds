# coding: utf-8
"""
Plots the "results.csv" output comparing team Elo 
differences and eventual point totals.

"""
import pandas as pd
games=pd.read_csv('results.csv',names=['id','score','dDoS'])
import matplotlib.pyplot as plt
plt.plot(games['dDoS'],games['score'],'o')
pylab.savefig('score_vs_dos.png')
