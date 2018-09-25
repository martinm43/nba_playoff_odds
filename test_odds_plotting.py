# coding: utf-8
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

from mcss_nba import playoff_odds_calc
from pprint import pprint
from nba_database.queries import team_abbreviation

#Dates
a = datetime(2017,10,1)
b = datetime(2017,12,1)
season_year = 2018
team_labels = [team_abbreviation(i) for i in range(1,30)]

#Team ID
i=28

odds_list = []
x_odds = playoff_odds_calc(a,b,season_year)
x_odds = [x[0] for x in x_odds]
odds_list.append(x_odds)

dates_list=[]
dates_list.append(b)

while b < datetime(season_year,5,1):
    x_odds = playoff_odds_calc(a,b,season_year)
    x_odds = [x[0] for x in x_odds]
    odds_list.append(x_odds)
    dates_list.append(b)
    b = b + timedelta(days=1)
    
odds_array = np.asarray(odds_list)

#Get team data
team_data = odds_array[:,i]

plt.xlabel('Date')
plt.ylabel('Team Playoff Odds')
plt.title(team_abbreviation(i+1)+' Playoff Odds, '+str(season_year))

print("Length of dates list: "+str(len(dates_list)))
print("Length of odds list: "+str(len(team_data)))

plt.plot(dates_list,team_data)
plt.show()