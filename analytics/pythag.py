# coding: utf-8
#This file attempts to calculate "Pythagorean wins" using pts scored for and
#against a team in a given season. The default exponent is set to that 
#used by Basketball Reference, which compares favourably to the range given in 
#Basketball on Paper (Oliver)
from __future__ import division #this is a major key. Forces floating point div.
from pprint import pprint
import time
import sys
from tabulate import tabulate

def pythagorean_wins(Game,team_id_num,year_start_num,win_exp=14,numgames=82,\
			mincalcdate=0.0,\
			maxcalcdate=999999999999.9,\
			source_option='bballref_scores'):
    """
    Game: a peewee ORM object passed from a main file.
    """
    team_id=str(team_id_num)
    year_start=str(year_start_num)
    if source_option=='bballref_scores':
	    pts=Game.select(Game.away_pts).where(\
        	                 Game.away_team_id==team_id,\
                	         Game.season_year==year_start,\
				 Game.datetime>=mincalcdate,\
				 Game.datetime<=maxcalcdate)
	    team_away_pts=sum([p.away_pts for p in pts])

	    pts=Game.select(Game.home_pts).where(\
        	                 Game.home_team_id==team_id,\
                	         Game.season_year==year_start,\
				 Game.datetime>=mincalcdate,\
				 Game.datetime<=maxcalcdate)

	    team_home_pts=sum([p.home_pts for p in pts if p.home_pts is not None])
	    team_pts_for=team_away_pts+team_home_pts

	    team_pts_against_home=Game.select(Game.away_pts).where(\
        	                                       Game.home_team_id==team_id,\
                	                               Game.season_year==year_start,\
							 Game.datetime>=mincalcdate,\
     			        	               Game.datetime<=maxcalcdate)
	    team_pts_against_away=Game.select(Game.home_pts).where(\
        	                                       Game.away_team_id==team_id,\
                	                               Game.season_year==year_start,\
							 Game.datetime>=mincalcdate,\
     			        	               Game.datetime<=maxcalcdate)
	    team_pts_against_home=sum([p.away_pts for p in team_pts_against_home if p.away_pts is not None])
	    team_pts_against_away=sum([p.home_pts for p in team_pts_against_away if p.home_pts is not None])
	    team_pts_against=team_pts_against_away+team_pts_against_home

    if team_pts_against >0 and team_pts_for >0:
      return numgames*team_pts_for**win_exp/(team_pts_for**win_exp+team_pts_against**win_exp)
    else:
      return 0

def league_pythagorean_wins(season_year,mincalcdate,maxcalcdate,source_option="bballref_scores",win_exp=16.5):
  results_list=[]
  for i in range(1,31):
    results_list.append([team_abbreviation(i),pythagorean_wins(i,season_year,win_exp=win_exp,source_option=source_option\
    ,mincalcdate=epochtime(mincalcdate),maxcalcdate=epochtime(maxcalcdate))])
  return sorted(results_list, key=lambda x: x[1])


if __name__=='__main__':
  results_list=[]
  for i in range(1,31):
    results_list.append([team_abbreviation(i),pythagorean_wins(i,2018,win_exp=16.5,source_option="bballref_scores"\
    ,mincalcdate=epochtime(sys.argv[1]),maxcalcdate=epochtime(sys.argv[2]))])
  
  results_list=[[i[0],'{:.0f}'.format(i[1])] for i in results_list]
  table=tabulate(sorted(results_list, key=lambda x: x[1]),headers=["Team (abbrev.)","Number of Wins by Pythagorean Win Expectation"]) 
  print table
