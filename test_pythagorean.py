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
start_datetime = datetime(2007,10,01)
end_datetime = datetime(2008,04,30)

games_list=games_query(start_datetime,end_datetime)

#pprint(games_won_query(games_list, return_format="matrix"))

#Pythagorean Wins Testing
lpw_results = league_pythagorean_wins(Game,mincalcdatetime=epochtime(start_datetime),\
            maxcalcdatetime=epochtime(end_datetime))

lpw_tuples = [(team_abbreviation(x[0]),round(x[1],0)) for x in lpw_results]
results_table = tabulate(
        lpw_tuples,
        headers=[
            'Team',
            'Pythag. Wins'],
        tablefmt='rst',
        numalign='left')

print("Pythagorean Win Expectations \n"+\
        "Based on Games Played Between: "+start_datetime.strftime('%b %d %Y')+\
        " and "+end_datetime.strftime('%b %d %Y'))
print(results_table)