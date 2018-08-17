from __future__ import division, print_function
#Standard imports
from datetime import datetime
from pprint import pprint
#Query imports
from nba_database.queries import games_query
from nba_database.nba_data_models import BballrefScores as Game
from nba_database.supports import epochtime
#Analytics imports
from analytics.SRS import SRS
from analytics.pythag import pythagorean_wins

start_datetime = datetime(1997,01,01)
end_datetime = datetime(2016,03,31)

games_list=games_query(start_datetime,end_datetime)

#pprint(SRS(games_list))

print(pythagorean_wins(Game,28,mincalcdatetime=epochtime(start_datetime),\
              maxcalcdatetime=epochtime(end_datetime)))
