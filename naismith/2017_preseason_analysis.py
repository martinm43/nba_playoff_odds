# coding: utf-8
from dbtools.nba_data_models import NbaPyApiData
from dbtools.access_nba_data import stringtime, epochtime
starttime=epochtime('Sep 30 2017')
endtime=epochtime("Oct 14 2017")
    
s=NbaPyApiData.select(NbaPyApiData.away_standard,NbaPyApiData.away_pts,NbaPyApiData.home_standard,NbaPyApiData.home_pts).where(NbaPyApiData.day_datetime>=starttime,NbaPyApiData.
day_datetime<=endtime)

    
preseason_games=[(i.away_standard,i.away_pts,i.home_standard,i.home_pts) for i in s]

preseason_games_fixed=[i for i in preseason_games if i[0]>0 and i[2]>0]
preseason_games_fixed

from analytics.burke_solver import burke_calc
burke_calc(preseason_games_fixed)
preseason_games_fixed
