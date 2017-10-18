# coding: utf-8
from dbtools
from dbtools.nba_data_models
from dbtools.nba_data_models import NbaPyApiData
from dbtools.access_nba_data import stringtime, epochtime
starttime=epochtime('Sep 30 2017')
endtime=epochtime("Oct 14 2017')
endtime=epochtime("Oct 14 2017")
s=NbaPyApiData.select()
s=NbaPyApiData.select().where(NbaPyApiData.day_datetime>=starttime,NbaPyApiData.
day_datetime<=endtime)
for i in s:
    print i.id
    
dir(s[0])
s=NbaPyApiData.select(away_standard,away_pts,home_standard,home_pts).where(NbaPyApiData.day_datetime>=starttime,NbaPyApiData.
day_datetime<=endtime)
s=NbaPyApiData.select(NbaPyApiData.away_standard,NbaPyApiData.away_pts,NbaPyApiData.home_standard,NbaPyApiData.home_pts).where(NbaPyApiData.day_datetime>=starttime,NbaPyApiData.
day_datetime<=endtime)
for i in s:
    print(dir(i))
    
preseason_games=[i.away_standard,i.away_pts,i.home_standard,i.home_pts for i in s]

    
preseason_games=[(i.away_standard,i.away_pts,i.home_standard,i.home_pts) for i in s]


    
preseason_games
del preseason_games[7]
preseason_games
for i in preseason_games:
    if i[0] or i[2]:
        print i
        
for i in preseason_games:
    if i[0]==0 or i[2]==0:
        print i
        
        
preseason_games_fixed=[i for i in preseason_games if if i[0]>0 or i[2]>0]
preseason_games_fixed=[i for i in preseason_games if i[0]>0 or i[2]>0]
preseason_games_fixed
preseason_games_fixed=[i for i in preseason_games if i[0]>0 and i[2]>0]
preseason_games_fixed
from anaytics.burke_solver import burke_calc
from analytics.burke_solver import burke_calc
burke_calc(preseason_games_fixed)
burke_calc(preseason_games_fixed,impmode=None)
burke_calc(preseason_games_fixed)
preseason_games_fixed
