# coding: utf-8
from __future__ import division
from pprint import pprint
import numpy as np
from dbtools.nba_data_models import NbaPyApiData, BballrefScores
from dbtools.access_nba_data import epochtime, stringtime
from DoS_optimization import dos,expected_dos

#defaults
init_rank=1500 #what a "neutral team" is valued at
dos_factor=1.5 #factor applied to change value based on expected performance vs actual
def_env_factor=.75 #environment factor for away team
def_expect_factor=1.0 #affects sigmoid plot of -1 to +1 outcomes based on quality diff.

#arrays
ranks=np.ones(30)*init_rank

start_date=epochtime('Oct 1 1996')
end_date=epochtime('May 1 2017')

s=NbaPyApiData.select().where(NbaPyApiData.day_datetime>=start_date,\
                                NbaPyApiData.day_datetime<=end_date)

s_b=BballrefScores.select().where(BballrefScores.datetime>=start_date,\
                                BballrefScores.datetime<=end_date)


#nba py api version
#s_array=[(i.away_standard,i.away_pts,i.home_standard,i.home_pts) for i in s]
#bballref version
s_array=[(i.away_team_id,i.away_pts,i.home_team_id,i.home_pts) for i in s_b]
s_date_array=[(i.datetime) for i in s_b]

error=0

for i in s_array:
    if i[1]>0 and i[3]>0:
        away_rank=ranks[i[0]-1]
        home_rank=ranks[i[2]-1]
        expected_away_diff=expected_dos(away_rank,home_rank,env_factor=def_env_factor,expect_factor=def_expect_factor)
        expected_home_diff=expected_dos(home_rank,away_rank,env_factor=def_env_factor,expect_factor=def_expect_factor)
        away_diff=dos_factor*(dos(i[1],i[3])-expected_away_diff)
        home_diff=dos_factor*(dos(i[3],i[1])-expected_home_diff)
        error+=(dos(i[1],i[3])-expected_away_diff)**2+(dos(i[3],i[1])-expected_home_diff)**2
        ranks[i[0]-1]=away_rank+away_diff
        ranks[i[2]-1]=home_rank+home_diff
        for j in enumerate(ranks):
            print [j[0]+1,j[1]]
    
#print error
