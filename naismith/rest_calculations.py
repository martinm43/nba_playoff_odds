# coding: utf-8
# New rest calculation script. #
from dbtools.nba_data_models import BballrefScores as bbrs
import numpy as np
from string_conversion_tools import team_abbreviation
from dbtools.access_nba_data import stringtime

team=1
season_year=2018

rest_keys=['game_id','rest']
    
team_games=bbrs.select().where((bbrs.season_year==season_year) & ((bbrs.away_team_id==team) | (bbrs.home_team_id==team))).order_by(bbrs.datetime)

game_date_list=[[i.id,i.datetime] for i in team_games]
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

print(rest_dicts)
#print(rest_list)
