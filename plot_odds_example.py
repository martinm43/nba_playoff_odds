# coding: utf-8
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

from mcss_nba import playoff_odds_calc
from pprint import pprint

a = datetime(2016,10,1)
b = datetime(2016,12,1)
season_year = 2017

odds_list = []
x_odds = playoff_odds_calc(a,b,season_year)
x_odds = [x[0] for x in x_odds]

while b < datetime(season_year,5,1):
    b = b + timedelta(days=1)
    x_odds = playoff_odds_calc(a,b,season_year)
    x_odds = [x[0] for x in x_odds]
    odds_list.append(x_odds)

plt.xlabel('Date')
plt.ylabel('Change of Making Playoffs')

#plt.legend()

plt.plot(odds_list)
plt.show()