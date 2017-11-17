# coding: utf-8
from dbtools.nba_data_models import BballrefScores as bbrs
import numpy as np

team=1
season_year=2018
    
team_games=bbrs.select().where((bbrs.season_year==season_year) & ((bbrs.away_team_id==team) | (bbrs.home_team_id==team)))

game_date_list=[[i.id,i.datetime] for i in team_games]

game_date_list[1:] #all games except the first one
game_date_list[0][0] #first game id
