from nba_database.queries import games_query
from datetime import datetime
from pprint import pprint

start_datetime = datetime(2016,01,01)
end_datetime = datetime(2016,03,31)

pprint(games_query(start_datetime,end_datetime))
