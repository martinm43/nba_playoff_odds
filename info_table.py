from __future__ import division, print_function
#Standard imports
from datetime import datetime
from pprint import pprint
#Third Party Imports
from tabulate import tabulate
#Query imports
from nba_database.queries import games_query, team_abbreviation, games_won_query, epochtime
from nba_database.nba_data_models import BballrefScores as Game
#Analytics imports
from analytics.SRS import SRS
from analytics.pythag import pythagorean_wins, league_pythagorean_wins

#Query Testing
start_datetime = datetime(2018,10,01)
end_datetime = datetime(2018,11,01)

games_list=games_query(start_datetime,end_datetime)

#Custom SRS calculation options
max_MOV = 10
home_team_adv = 2.5
win_floor = 5

#Pythagorean Wins
lpw_results = league_pythagorean_wins(Game,mincalcdatetime=epochtime(start_datetime),\
            maxcalcdatetime=epochtime(end_datetime))

srs_list = SRS(games_list, max_MOV = max_MOV, home_team_adv = home_team_adv, win_floor = win_floor)

lpw_results.sort(key = lambda x:x[0])

results = zip(lpw_results,srs_list)

results = [[x[0][0],x[0][1],x[1]] for x in results]

pprint(results)

results_tuples = [(team_abbreviation(x[0]),round(x[1],0),round(x[2]*100.0/100.0,3)) for x in results]

results_tuples.sort(key = lambda x:-x[2])

results_table = tabulate(
        results_tuples,
        headers=[
            'Team',
            'Pythag. Wins',
            'Est. SRS'],
        tablefmt='rst',
        numalign='left')

print("Pythagorean Win Expectations \n"+\
        "Based on Games Played Between: "+start_datetime.strftime('%b %d %Y')+\
        " and "+end_datetime.strftime('%b %d %Y'))
print(results_table)
