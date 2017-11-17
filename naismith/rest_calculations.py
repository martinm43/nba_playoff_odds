# coding: utf-8
# New rest calculation script. #
from dbtools.nba_data_models import BballrefScores as bbrs
from dbtools.nba_data_models import BballrefRest, database
from dbtools.max_sql_variables import max_sql_variables
SQLITE_MAX_VARIABLE_NUMBER=max_sql_variables()
import numpy as np
from string_conversion_tools import team_abbreviation
from dbtools.access_nba_data import stringtime
from pprint import pprint

rest_keys=['game_id','rest']

team=18
season_year=2007

for season_year in range(2007,2008):
 season_dicts=[]
 season_count=0
 for team in range(1,31):
   team_games=bbrs.select().where((bbrs.season_year==season_year) & ((bbrs.away_team_id==team) | (bbrs.home_team_id==team))).order_by(bbrs.datetime)

   game_date_list=[[i.id,i.datetime] for i in team_games]

   if len(game_date_list)>0:

        game_date_array=np.asarray(game_date_list) 

        rest_array=np.zeros_like(game_date_array)
        rest_array[0,:]=np.asarray([game_date_array[0,0],24*7.0])

        for i in range(1,len(game_date_array)):
            #print(game_date_array[i,:])
            rest_array[i,0]=game_date_array[i,0]
            rest_array[i,1]=game_date_array[i,1]-game_date_array[i-1,1]
            rest_array[i,1]=rest_array[i,1]/3600.0 #to hours
            if rest_array[i,1]<0:
                print(stringtime(game_date_array[i,1]))
                print(stringtime(game_date_array[i-1,1]))

        rest_list=rest_array.tolist()
        rest_dicts=[dict(zip(rest_keys,i)) for i in rest_list]
        for i in rest_dicts:
            i['team_id']=team
            i['id']=season_year*10000+season_count
            i['season_year']=season_year
            season_count+=1
            season_dicts.append(i)

 with database.atomic() as txn:
   size = (SQLITE_MAX_VARIABLE_NUMBER // len(season_dicts[0])) - 1                                               # remove one to avoid issue if peewee adds some variable
   for i in range(0, len(season_dicts), size):
     BballrefRest.insert_many(season_dicts[i:i+size]).upsert().execute()
