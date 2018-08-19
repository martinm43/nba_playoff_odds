# coding: utf-8
from datetime import datetime, timedelta
from mcss_nba import playoff_odds_calc
from pprint import pprint

a = datetime(2014,10,1)
b = datetime(2014,12,1)
season_year = 2014

odds_list = []
x_odds = playoff_odds_calc(a,b,season_year)

while b < datetime(2015,5,1):
    b = b + timedelta(days=7)
    x_odds = playoff_odds_calc(a,b,season_year)
    odds_list.append(x_odds)
    
pprint(odds_list)