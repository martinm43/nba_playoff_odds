# coding: utf-8
"""
A script that plots the playoff odds for a given division and given "season_year".

Inputs:
    season_year - can be randomized (random.randint) or user-selected
    division_name - can be randomized (random.choice) or user-selected
    
    Constants: max_year and min_year
    
Output:
    A bitmap image plot of the playoff odds 
    for a given division and given "season_year"

"""
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pprint import pprint 

import random

from prediction_table import playoff_odds_calc

from nba_database.queries import team_abbreviation
from nba_database.nba_data_models import ProApiTeams

division_name_list = ["Atlantic", "Central", "Southeast", "Southwest", "Pacific", "Northwest"]


try:
    season_year = int(input("Please select a year between 1990 and 2023, or enter 0 for random year: "))
except ValueError:
    print("Invalid value entered, quitting!!")
    sys.exit(1)
    0

min_year = 1990
max_year = 2023

if season_year == 0:
    season_year = random.randint(min_year,max_year)
    print("Random year selected is "+str(season_year))
if season_year < min_year or season_year > max_year:
    print("Year outside range, exiting!")
    sys.exit(1)


elif season_year == 2012:  # 2011-2012 lockout year fix.
    a = datetime(season_year - 1, 12, 25)
    b = datetime(season_year, 1, 15)
    end = datetime(season_year, 5, 30)
elif season_year == 1999:  # 1998-1999 lockout year fix.
    a = datetime(season_year, 2, 5)
    b = datetime(season_year, 2, 26)
    end = datetime(season_year, 5, 30)
elif season_year == 2020:  # Ft. The Day The World Stopped, 11 Mar 2020
    a = datetime(season_year-1, 10, 1)
    b = datetime(season_year-1, 11, 15)
    end = datetime(season_year, 8, 14)
elif season_year == 2021:  # SARS-CoV-2 fix (Second Season)
    a = datetime(season_year - 1, 12, 25)
    b = datetime(season_year, 1, 15)
    end = min(datetime(season_year, 5, 30),datetime.today() - timedelta(days=1))
else:
    a = datetime(season_year - 1, 10, 1)
    b = datetime(season_year - 1, 11, 15)
    end = min(datetime(season_year, 4, 30), datetime.today() - timedelta(days=1))


# Python Moving Average, taken by:
# https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
# note that there's a faster version using pandas but NO PANDAS.
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / N


team_labels = [team_abbreviation(i) for i in range(1, 30)]

# Team ID
# Possible divisions are Southeast, Atlantic, Central
# Pacific, Southwest, Northwest
print("Divisions are as follows: ")
print(" 1: Atlantic \n 2: Central \n 3: Southeast \n 4: Southwest \n 5: Pacific \n 6: Northwest")
dn = input("Please select a division: ")

try:
    division_number = int(dn)-1
except:
    print("invalid input for division number, not integer")
    sys.exit(1)
try:
    division_name = division_name_list[division_number]
except IndexError:
    print("out of range for divisions, program exiting")
    sys.exit(1)

query = ProApiTeams.select().where(ProApiTeams.division == division_name)
division_team_id_list = [i.bball_ref for i in query]


# Odds calculations
odds_list = []
x_odds = playoff_odds_calc(a, b, season_year)
print("Calculation modes are as follows: ")
print("1: Classic mode (top 8 finish)\n2: Top 6 mode\n3: Top 10 mode")
mode_dict={1:"Top 8",2:"Top 6",3:"Top 10"}
mode = input("Please select a calculation mode: ")
try:
    mode = int(mode)
except:
    print("not an integer, exiting now")
    sys.exit(1)

if mode == 1:
    x_odds = [x[0] for x in x_odds]
elif mode == 2:
    x_odds = [x[2] for x in x_odds]
elif mode == 3:
    x_odds = [x[2]+x[3] for x in x_odds]
else:
    print("mode invalid, quitting")
    sys.exit(1)

odds_list.append(x_odds)

dates_list = []
dates_list.append(b)

ratings_mode = "SRS"


while b < end:
    
    x_odds = playoff_odds_calc(a, b, season_year, ratings_mode=ratings_mode)

    #print(b)
    #pprint(x_odds)

    if mode == 1:
        x_odds = [x[0] for x in x_odds]
    elif mode == 2:
        x_odds = [x[2] for x in x_odds]
    elif mode == 3:
        x_odds = [x[2]+x[3] for x in x_odds]


    print("Finished processing "+b.strftime("%m %d %Y"))

    odds_list.append(x_odds)
    dates_list.append(b)
    b = b + timedelta(days=1) #1



odds_array = np.asarray(odds_list)

plt.figure(figsize=(10, 10))
plt.ylim(-5, 105)  # so 100 shows up on the graph, and 0 (thanks V.)

# Get team data
for team_id_db in division_team_id_list:
    team_id = team_id_db - 1
    team_data = odds_array[:, team_id]
    N = len(team_data)
    average_count = 1 #so playoff odds converge to 1.
    average_team_data = running_mean(team_data, average_count)
    average_dates_list = dates_list[average_count - 1 :]
    # plt.plot(dates_list,team_data)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
    plt.plot(
        average_dates_list,
        average_team_data,
        label=team_abbreviation(team_id + 1),
        alpha=0.6,
    )

plt.xlabel("Date")
plt.ylabel("Team Playoff Odds")
plt.title(
    division_name
    + " Division Playoff Odds "
+ str(season_year - 1)
+ "-"
+ str(season_year)
+ "\n (teams in division may not be accurate before 2004, "+mode_dict[mode]+")"
)
plt.legend()
plt.xticks(rotation=15)
plt.savefig(division_name + "_" + str(season_year) + ".png")
plt.show()
