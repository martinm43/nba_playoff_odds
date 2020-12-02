# coding: utf-8

import numpy as np

from random import randint
from nba_database.queries import season_query, team_elo_rating
from analytics.morey import Elo_regress

for year in range(1990,2021):
    season_query(year)
    games = season_query(year)
    success_rate = []

    for z in games:
        elo_diff = team_elo_rating(z[2],z[4])-team_elo_rating(z[0],z[4])
        elo_odds = Elo_regress(elo_diff)
        pts_diff = z[3]-z[1]
        if (elo_odds > 0.5 and pts_diff > 0) or (elo_odds <= 0.5 and pts_diff < 0):
            success_rate.append(1)
        else:
            success_rate.append(0)
        
        
    sr_array = np.asarray(success_rate)
    success_rate = np.sum(sr_array)/sr_array.size*100

    success_rate_string = "%.1f" % success_rate

    print("Accuracy in year "+str(year)+": "+success_rate_string+"%")
