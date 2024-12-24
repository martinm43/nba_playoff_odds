# -*- coding: utf-8 -*-
"""
To do: combine with the concept of games, maybe? Data needs to be munged maybe
but this is a good toy script for understanding what can be done 
using automation
"""

import json

from datetime import datetime, timedelta
from pprint import pprint
from nba_database.nba_data_models import BballrefScores
from nba_database.queries import abbrev_to_id

from nba_api.stats.endpoints import scoreboardv2



start_date = datetime.today() - timedelta(days=5)
end_date = datetime.today()
loop_date = start_date

while loop_date < end_date:
    
    game_date = loop_date.strftime("%Y-%m-%d")
    print("Processing date "+game_date) 
    games = scoreboardv2.ScoreboardV2(game_date=game_date)
    games_json=json.loads(games.get_json())
    
    # Reforming dicts of required data based on game results, identified by team abbrev
    datalist = games_json["resultSets"][1]["rowSet"]
    results = []
        
    game_list = []
    #Master list for determining what is in the api 
    #7: record entering the game
    #8,9,10,11: 1q 2q 3q 4q
    #23: FG%
    #24: FT%
    #25: 3P%
    #26: total assists
    #27: total rebounds
    #28: blocks
    for i in range(0, len(datalist), 2):  # Step by 2 to process each pair
        game = {
            "away_team_id": abbrev_to_id(datalist[i][4]),           # Away team data
            "home_team_id": abbrev_to_id(datalist[i + 1][4]),        # Home team data
            "away_pts": datalist[i][22],           # Away team data
            "home_pts": datalist[i + 1][22],        # Home team data
            "game_date": datalist[i][0][0:10],           # Away team data
            "1Q_Away":datalist[i][8], #kept for an example
            "1Q_Home":datalist[i + 1][8] #kept for an example
        }
        pprint(game)
        game_list.append(game)

        
    for z in game_list: 
        BballrefScores.update(away_pts = z["away_pts"], home_pts = z["home_pts"]).\
            where((BballrefScores.date == z["game_date"]) & \
                  (BballrefScores.away_team_id == z["away_team_id"]) & \
                  (BballrefScores.home_team_id == z["home_team_id"])).execute()

        
    print("Processing date "+game_date+" complete.") 
    loop_date = loop_date + timedelta(days=1)
