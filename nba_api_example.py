# coding: utf-8
from datetime import datetime
from pprint import pprint

from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2

from nba_database.queries import epochtime, abbrev_to_id

x_date=datetime(2018,10,16)
s = ScoreboardV2(game_date=x_date)

day_results=s.line_score.get_dict()
day_results_data=[dict(zip(day_results['headers'],x)) for x in day_results['data']]

game_dict={}
for i in range(0,len(day_results_data),2):
    print(i)
    pprint(day_results_data[0])
    game_dict['away_pts'] = day_results_data[0]['PTS']
    game_dict['away_team_id'] = abbrev_to_id(day_results_data[0]['TEAM_ABBREVIATION'])
    game_dict['datetime'] = epochtime(x_date)
    pprint(game_dict)
