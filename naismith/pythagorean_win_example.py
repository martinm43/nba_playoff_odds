# coding: utf-8
#This file attempts to calculate "Pythagorean wins" using pts scored for and
#against a team in a given season. The default exponent is set to that 
#used by Basketball Reference, which compares favourably to the range given in 
#Basketball on Paper (Oliver)
from __future__ import division #this is a major key. Forces floating point div.

from dbtools.nba_data_models import BballrefScores, NbaPyApiData
from string_conversion_tools import team_abbreviation

def pythagorean_wins(team_id_num,year_start_num,win_exp=14,numgames=82,\
			mincalcdate=0.0,\
			maxcalcdate=999999999999.9,\
			source_option='bballref_scores'):

    team_id=str(team_id_num)
    year_start=str(year_start_num)
    if source_option=='bballref_scores':
	    pts=BballrefScores.select(BballrefScores.away_pts).where(\
        	                 BballrefScores.away_team_id==team_id,\
                	         BballrefScores.season_year==year_start,\
				 BballrefScores.datetime>mincalcdate,\
				 BballrefScores.datetime<maxcalcdate)
	    team_away_pts=sum([p.away_pts for p in pts])

	    pts=BballrefScores.select(BballrefScores.home_pts).where(\
        	                 BballrefScores.home_team_id==team_id,\
                	         BballrefScores.season_year==year_start,\
				 BballrefScores.datetime>mincalcdate,\
				 BballrefScores.datetime<maxcalcdate)

	    team_home_pts=sum([p.home_pts for p in pts if p.home_pts is not None])
	    team_pts_for=team_away_pts+team_home_pts

	    team_pts_against_home=BballrefScores.select(BballrefScores.away_pts).where(\
        	                                       BballrefScores.home_team_id==team_id,\
                	                               BballrefScores.season_year==year_start,\
							 BballrefScores.datetime>mincalcdate,\
     			        	               BballrefScores.datetime<maxcalcdate)
	    team_pts_against_away=BballrefScores.select(BballrefScores.home_pts).where(\
        	                                       BballrefScores.away_team_id==team_id,\
                	                               BballrefScores.season_year==year_start,\
							 BballrefScores.datetime>mincalcdate,\
     			        	               BballrefScores.datetime<maxcalcdate)
	    team_pts_against_home=sum([p.away_pts for p in team_pts_against_home if p.away_pts is not None])
	    team_pts_against_away=sum([p.home_pts for p in team_pts_against_away if p.home_pts is not None])
	    team_pts_against=team_pts_against_away+team_pts_against_home

    elif source_option=='nba_py_api_data': #under development
	    #"minimum and maximum calc date" logic not working. Temp fix made
            pts=NbaPyApiData.select().where(NbaPyApiData.away_standard==team_id,NbaPyApiData.season_year==year_start)
	    team_away_pts=sum([p.away_pts for p in pts if p.away_pts is not None])
            
            pts=NbaPyApiData.select().where(NbaPyApiData.home_standard==team_id,NbaPyApiData.season_year==year_start)
            team_home_pts=sum([p.home_pts for p in pts if p.home_pts is not None])
	    
            team_pts_for=team_away_pts+team_home_pts

	    team_pts_against_home=NbaPyApiData.select().where(NbaPyApiData.home_standard==team_id,NbaPyApiData.season_year==year_start)	    
	    team_pts_against_home=sum([p.away_pts for p in team_pts_against_home if p.away_pts is not None])
            
            team_pts_against_away=NbaPyApiData.select().where(NbaPyApiData.away_standard==team_id,NbaPyApiData.season_year==year_start)
	    team_pts_against_away=sum([p.home_pts for p in team_pts_against_away if p.home_pts is not None])

	    team_pts_against=team_pts_against_away+team_pts_against_home

    if team_pts_against >0 and team_pts_for >0:
      return numgames*team_pts_for**win_exp/(team_pts_for**win_exp+team_pts_against**win_exp)
    else:
      return 0

if __name__=='__main__':
  for i in range(1,31):
    print([team_abbreviation(i),pythagorean_wins(i,2018,source_option="nba_py_api_data")])
