# -*- coding: utf-8 -*-
"""
To do: combine with the concept of games, maybe? Data needs to be munged maybe
but this is a good toy script for understanding what can be done 
using automation
"""

import json

from datetime import datetime, timedelta
from nba_database.nba_data_models import BballrefScores
from nba_database.queries import abbrev_to_id

from nba_api.stats.endpoints import scoreboardv3



start_date = datetime.today() - timedelta(days=30)
end_date = datetime.today()
loop_date = start_date

while loop_date < end_date:

    game_date = loop_date.strftime("%Y-%m-%d")
    print("Processing date "+game_date) 
    games = scoreboardv3.ScoreboardV3(game_date=game_date)
    games_json=json.loads(games.get_json())
    #fname = f"responses/{datetime.now().isoformat()}.json"
    #with open(fname, "w") as f:
    #    json.dump(games_json, f, indent=2)
    
    #pprint(games_json)
    z=games_json.keys()
    # Reforming dicts of required data based on game results, identified by team abbrev
    #print(games_json["scoreboard"].keys())
    datalist = games_json["scoreboard"]["games"]
    
    #print(datalist)
    results = []
        
    game_list = []
    
    for i in range(0, len(datalist)):  # Step by 2 to process each pair
        to_proc = datalist[i]
        game = {
            "away_abbrev": to_proc['awayTeam']['teamTricode'],
            "home_abbrev": to_proc['homeTeam']['teamTricode'],
            "away_team_id": abbrev_to_id(to_proc['awayTeam']['teamTricode']),           # Away team data
            "home_team_id": abbrev_to_id(to_proc['homeTeam']['teamTricode']),        # Home team data
            "away_pts": to_proc['awayTeam']['score'],           # Away team data
            "home_pts": to_proc['homeTeam']['score'],        # Home team data
            "game_date": datetime.fromisoformat(to_proc['gameEt'].replace("Z","+00:00")).strftime('%Y-%m-%d'),           # Away team data
        }
        print(game["away_abbrev"]+" "+str(game["away_pts"])+", "+game["home_abbrev"]+" "+str(game["home_pts"])+" on "+game["game_date"])
        game_list.append(game)
    
            
    for z in game_list: 
        BballrefScores.update(away_pts = z["away_pts"], home_pts = z["home_pts"]).\
            where((BballrefScores.date == z["game_date"]) & \
                    (BballrefScores.away_team_id == z["away_team_id"]) & \
                    (BballrefScores.home_team_id == z["home_team_id"])).execute()
    
        
    print("Processing date "+game_date+" complete.") 
    loop_date = loop_date + timedelta(days=1)


