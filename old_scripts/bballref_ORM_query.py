# coding: utf-8
from dbtools.nba_data_models import BballrefScores
from analytics.burke_solver import burke_calc

games=BballrefScores.select(BballrefScores.away_team_id,BballrefScores.away_pts,BballrefScores.home_team_id,BballrefScores.home_pts).where(BballrefScores.season_year==2017)
for g in games:
    print g.away_team_id,g.away_pts,g.home_team_id,g.home_pts
    
    
    
