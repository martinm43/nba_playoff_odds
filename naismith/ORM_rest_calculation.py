# coding: utf-8
from dbtools.rest_and_travel import team_rest_calc_v2
from dbtools.nba_data_models import BballrefScores

year=2017

g=BballrefScores.select().where(BballrefScores.season_year==year)
g_dicts=g.dicts()
rest_dicts=team_rest_calc_v2(g_dicts)

rest_dicts=team_rest_calc_v2(g_dicts)
rest_dicts[0]
