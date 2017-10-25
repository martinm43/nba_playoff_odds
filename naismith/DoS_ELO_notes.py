# coding: utf-8
from __future__ import division
from dbtools.access_nba_data import epochtime, stringtime
from dbtools.nba_data_models import NbaPyApiData
season_start_2018=epochtime('Oct 17 2017')
stringtime(season_start_2018)
s=NbaPyApiData.select().where(NbaPyApiData.day_datetime>season_start_2018)
for i in s:
    a=(i.away_pts-i.home_pts)/(i.away_pts+i.home_pts)
    print i.away_team_city_name,i.home_team_city_name, a

