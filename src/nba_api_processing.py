# -*- coding: utf-8 -*-
"""
To do: combine with the concept of games, maybe? Data needs to be munged maybe
but this is a good toy script for understanding what can be done 
using automation
"""

import json
from nba_api.stats.endpoints import scoreboard

game_date = "2023-01-26"

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
    game_list.append(game_dict)
    
#Usually BUT NOT ALWAYS in "Away@Home" format in the list of teams...
