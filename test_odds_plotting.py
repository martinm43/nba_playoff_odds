# coding: utf-8
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

from mcss_nba import playoff_odds_calc
from pprint import pprint
from nba_database.queries import team_abbreviation

# Python Moving Average, taken by:
# https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
# note that there's a faster version using pandas but NO PANDAS.
def running_mean(x, N):
   cumsum = np.cumsum(np.insert(x, 0, 0)) 
   return (cumsum[N:] - cumsum[:-N]) / N

#Dates
a = datetime(2016,10,1)
b = datetime(2016,12,1)
season_year = 2017
team_labels = [team_abbreviation(i) for i in range(1,30)]

#Team ID
#Atlantic division ids are 2, 3, 20, 23, 28.
#Southeast: 1, 16, 22, 30, 4
#Southwest: 10, 7, 11, 27, 15
#Pacific: 10, 13, 14, 24, 26
#Noethwest: 8, 18, 25, 21, 29
#Central: 6, 5, 17, 12, 9
division_team_id_list = [10,13,14,24,26]

#Odds calculations
odds_list = []
x_odds = playoff_odds_calc(a,b,season_year)
x_odds = [x[0] for x in x_odds]
odds_list.append(x_odds)

dates_list=[]
dates_list.append(b)

while b < datetime(season_year,4,15):
    x_odds = playoff_odds_calc(a,b,season_year)
    x_odds = [x[0] for x in x_odds]
    odds_list.append(x_odds)
    dates_list.append(b)
    b = b + timedelta(days=1)
    
odds_array = np.asarray(odds_list)

plt.figure(figsize=(7.5,7.5))
plt.ylim(0,105) #so 100 shows up on the graph.

#Get team data
for team_id_db in division_team_id_list:
    team_id=team_id_db-1
    team_data = odds_array[:,team_id]
    N = len(team_data)
    average_count = 5
    average_team_data = running_mean(team_data,average_count)
    average_dates_list = dates_list[average_count-1:]
    #plt.plot(dates_list,team_data)
    plt.plot(average_dates_list,average_team_data, label=team_abbreviation(team_id+1))

plt.xlabel('Date')
plt.ylabel('Team Playoff Odds')
plt.title('Atlantic Division Playoff Odds '+str(season_year-1)+'-'+str(season_year))
plt.legend()
plt.show()