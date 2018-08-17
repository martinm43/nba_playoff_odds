from __future__ import division, print_function
#Standard imports
from datetime import datetime
from pprint import pprint
#Query imports
from nba_database.queries import games_query, team_abbreviation
from nba_database.nba_data_models import BballrefScores as Game
from nba_database.supports import epochtime
#Analytics imports
from analytics.SRS import SRS
from analytics.pythag import pythagorean_wins, league_pythagorean_wins

start_datetime = datetime(2015,10,01)
end_datetime = datetime(2016,04,30)

games_list=games_query(start_datetime,end_datetime)

#pprint(SRS(games_list))

lpw_results = league_pythagorean_wins(Game,mincalcdatetime=epochtime(start_datetime),\
            maxcalcdatetime=epochtime(end_datetime))

lpw_results = [[team_abbreviation(x[0]),x[1]] for x in lpw_results]
pprint(lpw_results)
