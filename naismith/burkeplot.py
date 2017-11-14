# coding: utf-8
from burke_month_calc import burke_month_calc
from dbtools.access_nba_data import epochtime
from dbtools.nba_data_models import ProApiTeams
import numpy as np
import matplotlib.pyplot as plt

startdate=epochtime('Nov 15 2016')
enddate=epochtime('Apr 15 2017')

dates=np.linspace(startdate,enddate,300)
y=[burke_month_calc(i) for i in dates]

plt.title('Team Performances over 2017 season by burke_rating')
plt.ylabel('burke_rating')
plt.xlabel('Date')

s=ProApiTeams.select()
team_labels=sorted([i.abbreviation for i in s])

plt.legend(team_labels[:-1]) #get the "None" entry out
plt.plot(dates,y)
plt.show()