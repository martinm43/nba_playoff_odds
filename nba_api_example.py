# coding: utf-8
from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2
from datetime import datetime

s = ScoreboardV2(game_date=datetime(2018,10,16))

day_results=s.line_score.get_dict()

team_dicts=[dict(zip(day_results['headers'],d)) for d in day_results['data']]
