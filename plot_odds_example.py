# coding: utf-8
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

from mcss_nba import playoff_odds_calc
from pprint import pprint
from nba_database.queries import team_abbreviation

a = datetime(2016,10,1)
b = datetime(2016,12,1)
season_year = 2017
team_labels = [team_abbreviation(i) for i in range(1,30)]

odds_list = []
x_odds = playoff_odds_calc(a,b,season_year)
x_odds = [x[0] for x in x_odds]

dates_list=[]
dates_list.append(b)

while b < datetime(season_year,5,1):
    b = b + timedelta(days=1)
    x_odds = playoff_odds_calc(a,b,season_year)
    x_odds = [x[0] for x in x_odds]
    odds_list.append(x_odds)
    dates_list.append(b)
    
odds_array = np.asarray(odds_list)

plt.xlabel('Date')
plt.ylabel('Team Playoff Odds')
plt.title('NBA Team Playoff Odds, '+str(season_year))
plt.legend(handles=team_labels)

plt.plot(odds_array)
plt.show()