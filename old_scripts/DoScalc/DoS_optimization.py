# coding: utf-8
from __future__ import division
from pprint import pprint
import numpy as np
from dbtools.nba_data_models import NbaPyApiData, BballrefScores
from dbtools.access_nba_data import epochtime, stringtime
import matplotlib.pyplot as plt

#local function definitions
def dos(pts_a,pts_b):
    return (pts_a-pts_b)/(pts_a+pts_b)

def expected_dos(rank_a,rank_b,env_factor=2.0,expect_factor=0.025):
    return -1+2.0/(1+np.exp(-expect_factor*(rank_a-rank_b-env_factor)))

def DoS_calculation_error(s_array,def_env_factor, def_expect_factor,dos_factor=2):
    
    #defaults
    init_rank=1000 #what a "neutral team" is valued at
    
    #arrays
    ranks=np.ones(30)*init_rank

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

    return error

if __name__=='__main__':
    #input variables to function
    start_date=epochtime('Oct 1 2016')
    end_date=epochtime('May 1 2017')
    test_env_factor=2
    test_expect_factor=0.001
    s_b=BballrefScores.select().where(BballrefScores.datetime>=start_date,\
                                BballrefScores.datetime<=end_date)
    #Convert into universal format
    s_array=[(i.away_team_id,i.away_pts,i.home_team_id,i.home_pts) for i in s_b]

    test_values=np.linspace(0.000,0.006,100) #value appears to be on the order of 0.01?

    #Crude investigation into the possible ranges of "ideal values"
    plt.figure()
    ave_game_errors=[(i,np.sqrt(DoS_calculation_error(s_array,.75,i)/(2*len(s_array)))) for i in test_values]
    ave_game_errors=np.asarray(ave_game_errors)
    #for i in ave_game_errors:
    #	  print i
    plt.plot(ave_game_errors[:,0],ave_game_errors[:,1])

    #Plot the probability charts for a win and for a loss (expected range of scores)
    dos_differences=np.linspace(-300,300)
    y=[expected_dos(i,0,env_factor=test_env_factor,expect_factor=test_expect_factor) for i in dos_differences]
    plt.figure()
    plt.plot(dos_differences,y)
    plt.show()