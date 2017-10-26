# coding: utf-8
from __future__ import division
from pprint import pprint
import numpy as np
from dbtools.nba_data_models import NbaPyApiData
from dbtools.access_nba_data import epochtime, stringtime

#defaults
init_rank=750 #what a "neutral team" is valued at
dos_factor=10 #factor applied to change value based on expected performance vs actual
def_env_factor=0.6 #environment factor for away team
#The trickiest factor
def_expect_factor=0.5 #affects sigmoid plot of -1 to +1 outcomes based on quality diff.
#how much does talent disparity affect expected "win ratio"?

#arrays
ranks=np.ones(30)*init_rank

#local function definitions
def dos(pts_a,pts_b):
    return (pts_a-pts_b)/(pts_a+pts_b)

def expected_dos(rank_a,rank_b,env_factor=def_env_factor,expect_factor=def_expect_factor):
    return -1+expect_factor/(1+np.exp(rank_a-rank_b-env_factor))

start_date=epochtime('Oct 1 2016')
end_date=epochtime('May 1 2017')
stringtime(season_start_2018)

s=NbaPyApiData.select().where(NbaPyApiData.day_datetime>=start_date,\
                                NbaPyApiData.day_datetime<=end_date)
#s=NbaPyApiData.select()

for i in s:
    if i.away_pts>0 and i.home_pts>0:
        away_rank=ranks[i.away_standard-1]
        home_rank=ranks[i.home_standard-1]
        expected_away_diff=expected_dos(away_rank,home_rank)
        expected_home_diff=expected_dos(home_rank,away_rank)
        print([expected_away_diff,expected_home_diff])
        away_diff=dos_factor*(dos(i.away_pts,i.home_pts)-expected_away_diff)
        home_diff=dos_factor*(dos(i.home_pts,i.away_pts)-expected_home_diff)
        ranks[i.away_standard-1]=away_rank+away_diff
        ranks[i.home_standard-1]=home_rank+home_diff
        print i.away_team_city_name,i.home_team_city_name
        for j in enumerate(ranks):
            print [j[0]+1,j[1]]
    
