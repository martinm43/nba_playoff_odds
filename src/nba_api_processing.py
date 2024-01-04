# -*- coding: utf-8 -*-
"""
To do: combine with the concept of games, maybe? Data needs to be munged maybe
but this is a good toy script for understanding what can be done 
using automation
"""

import json

from datetime import datetime, timedelta

from nba_database.nba_data_models import database, BballrefScores
from nba_database.queries import epochtime, abbrev_to_id

from nba_api.stats.endpoints import scoreboard



start_date = datetime.today() - timedelta(days=7)
end_date = datetime.today() - timedelta(days=1)
loop_date = start_date

while loop_date < end_date:
    
    game_date = loop_date.strftime("%Y-%m-%d")
    print("Processing date "+game_date) 
    games = scoreboard.Scoreboard(game_date=game_date)
    games_json=json.loads(games.get_json())
    
    # Reforming dicts of required data based on game results, identified by team abbrev
    datalist = games_json["resultSets"][1]["rowSet"]
    results = []
    for d in datalist:
        results.append({"team_abbreviation":d[4],"pts":d[21]})
    
    # Attach team info as appropriate
    gameinfolist = games_json["resultSets"][0]["rowSet"]
    game_list = []
    for i in gameinfolist:
        game_str = i[5].split("/")[1]
        game_dict = {"away_team_abbreviation":game_str[0:3],"home_team_abbreviation":game_str[3:6]}
        away_pts = [x["pts"] for x in results if x["team_abbreviation"] == game_dict["away_team_abbreviation"]][0]
        home_pts = [x["pts"] for x in results if x["team_abbreviation"] == game_dict["home_team_abbreviation"]][0]
        game_dict["away_pts"]=away_pts
        game_dict["home_pts"]=home_pts
        game_dict["game_date"]=game_date
        try:
            game_dict["away_team_id"]=abbrev_to_id(game_dict["away_team_abbreviation"])
            game_dict["home_team_id"]=abbrev_to_id(game_dict["home_team_abbreviation"])
        except IndexError:
            print("Please review games on "+game_date+" between "+game_dict["away_team_abbreviation"]+" at "+game_dict["home_team_abbreviation"])
            game_dict["away_team_id"] = -1
            game_dict["home_team_id"] = -1
        
        
        game_dict["datetime"]=epochtime(datetime.strptime(game_dict["game_date"],"%Y-%m-%d"))
        game_list.append(game_dict)
        
    for z in game_list: 
        BballrefScores.update(away_pts = z["away_pts"], home_pts = z["home_pts"]).\
            where((BballrefScores.date == z["game_date"]) & \
                  (BballrefScores.away_team_id == z["away_team_id"]) & \
                  (BballrefScores.home_team_id == z["home_team_id"])).execute()

        
    print("Processing date "+game_date+" complete.") 
    loop_date = loop_date + timedelta(days=1)
