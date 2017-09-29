# coding: utf-8

import pandas as pd
def str_epochtime(str):
    import time
    from datetime import datetime
    return time.mktime(datetime.strptime(str,'%a %b %d %Y %I:%M %p').timetuple())

from max_sql_variables import max_sql_variables
SQLITE_MAX_VARIABLE_NUMBER=max_sql_variables()
from nba_data_models import *
from teamind import teamind
from pprint import pprint

games_2018=pd.read_csv('2018_season_schedule.csv')

#fillna issue
games_2018=games_2018.fillna(0)

games_2018['fulldate']=games_2018['date']+ ' '+games_2018['date_start_time_et']

games_2018['ot']=games_2018['OT']
del games_2018['OT']

games_2018['notes']=games_2018['Notes']
del games_2018['Notes']

games_2018['datetime']=games_2018['fulldate'].apply(lambda x: str_epochtime(x))

del games_2018['fulldate']
games_2018['start_time']=games_2018['date_start_time_et']
del games_2018['date_start_time_et']

#Use old nba name-to-id function to get ids.
games_2018['away_team_id']=games_2018['away_team'].apply(lambda x: teamind(x))
games_2018['home_team_id']=games_2018['home_team'].apply(lambda x: teamind(x))


#Create dictionaries.
games_2018_dicts=games_2018.T.to_dict().values()

#Add season year
ind=20180000
for i in games_2018_dicts:
    i['season_year']=2018
    i['id']=ind
    ind+=1


pprint(games_2018_dicts[0])

with database.atomic() as txn:
     size = (SQLITE_MAX_VARIABLE_NUMBER // len(games_2018_dicts[0])) - 1 
     # remove one to avoid issue if peewee adds some variable
     for i in range(0, len(games_2018_dicts), size):BballrefScores.insert_many(games_2018_dicts[i:i+size]).upsert().execute()
  

