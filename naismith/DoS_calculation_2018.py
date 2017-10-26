# coding: utf-8
# %load DoS_calculation_2018.py
# %load DoS_ELO_notes.py
from __future__ import division
from pprint import pprint
import numpy as np
init_rank=750
ranks=np.ones(30)*init_rank
dos_factor=40
from dbtools.access_nba_data import epochtime, stringtime
from dbtools.nba_data_models import NbaPyApiData
def dos(pts_a,pts_b):
    return (pts_a-pts_b)/(pts_a+pts_b)
def expected_dos(rank_a,rank_b,env_factor=def_env_factor):
    return  
season_start_2018=epochtime('Oct 17 2017')
stringtime(season_start_2018)
s=NbaPyApiData.select().where(NbaPyApiData.day_datetime>season_start_2018)
for i in s:
    away_diff=dos_factor*dos(i.away_pts,i.home_pts)
    home_diff=dos_factor*dos(i.home_pts,i.away_pts)
    ranks[i.away_standard-1]=ranks[i.away_standard-1]+away_diff
    ranks[i.home_standard-1]=ranks[i.home_standard-1]+home_diff
    print i.away_team_city_name,i.home_team_city_name
    pprint(ranks)
    
