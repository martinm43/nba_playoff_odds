from __future__ import division, print_function
#Standard imports
from datetime import datetime
from pprint import pprint
#Query imports
from nba_database.queries import games_query
#Analytics imports
from analytics.SRS import SRS

start_datetime = datetime(2016,01,01)
end_datetime = datetime(2016,03,31)

games_list=games_query(start_datetime,end_datetime)

pprint(SRS(games_list))
