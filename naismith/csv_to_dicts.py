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

games_2017=pd.read_csv('2017_season_complete.csv')
games_2017['fulldate']=games_2017['date']+ ' '+games_2017['date_start_time_et']

games_2017['ot']=games_2017['OT']
del games_2017['OT']

games_2017['notes']=games_2017['Notes']
del games_2017['Notes']

games_2017['datetime']=games_2017['fulldate'].apply(lambda x: str_epochtime(x))

del games_2017['fulldate']
games_2017['start_time']=games_2017['date_start_time_et']
del games_2017['date_start_time_et']

#Use old nba name-to-id function to get ids.
games_2017['away_team_id']=games_2017['away_team'].apply(lambda x: teamind(x))
games_2017['home_team_id']=games_2017['home_team'].apply(lambda x: teamind(x))

#fillna issue
games_2017.fillna('')

#Create dictionaries.
games_2017_dicts=games_2017.T.to_dict().values()

#Add season year
ind=20170000
for i in games_2017_dicts:
    i['season_year']=2017
    i['id']=ind
    ind+=1
    
with database.atomic() as txn:
     size = (SQLITE_MAX_VARIABLE_NUMBER // len(games_2017_dicts[0])) - 1 
     # remove one to avoid issue if peewee adds some variable
     for i in range(0, len(games_2017_dicts), size):BballrefScores.insert_many(games_2017_dicts[i:i+size]).upsert().execute()
  

