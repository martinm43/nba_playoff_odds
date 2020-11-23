
from nba_database.queries import season_query, team_abbreviation
from pprint import pprint
from math import exp
from random import randint
import numpy as np

default_rating = 0.2
default_HFA = 100
default_K = .005
scaling = 10000
season_elo_ratings_list = default_rating*np.ones((30,1))

def predicted_dos_formula(a,b):
    """
    Parameters
    ----------
    a : Elo rating of team a
    b : Elo rating of team b.
    
    Returns
    -------
    DoS : difference over sum estimate

    Constants
    ---------
    mean and stddev taken from results of points_analysis.py

    """
    mean = 0.015727
    stddev = 0.038081
    DoS = -1 + 2/(1+exp((b-a-mean)/stddev))
    return DoS

season_year = randint(1999,2021)
analysis_list = season_query(season_year)


for g in analysis_list:

    #get previous elo ratings
    away_rating = season_elo_ratings_list[g[0]-1]
    home_rating = season_elo_ratings_list[g[2]-1]
    #get expected DoS value, compare it to the real one
    expected_dos = predicted_dos_formula(away_rating, home_rating)
    actual_dos = ((g[1]-g[3])/(g[1]+g[3]))
    dos_difference = actual_dos - expected_dos

    change_factor = default_K*dos_difference
    season_elo_ratings_list[g[0]-1] = season_elo_ratings_list[g[0]-1]+change_factor
    season_elo_ratings_list[g[2]-1] = season_elo_ratings_list[g[2]-1]-change_factor
    

print("Final set of Elo ratings after season "+str(season_year)+" presented below.")

print_list=[]

for i,r in enumerate(season_elo_ratings_list):
    rtg = float(r[0]*scaling)
    team = team_abbreviation(i+1)
    print_list.append([rtg,team])
    
print_list = sorted(print_list,key=lambda x:-x[0])
top_list = print_list[0:10]
bottom_list = print_list[21:30]
print("Top 10 teams in "+str(season_year)+":")
for t in top_list:
    rating = "%.1f" % t[0]
    print(t[1]+": "+rating)
print("Bottom 10 teams in "+str(season_year)+":")
for t in bottom_list:
    rating = "%.1f" % t[0]
    print(t[1]+": "+rating)
