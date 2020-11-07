
from nba_database.queries import season_query, team_abbreviation
from pprint import pprint
from math import exp
import numpy as np


#defaults taken from https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/
default_rating = 1500
default_HFA = 100
default_K = 80
season_elo_ratings_list = default_rating*np.ones((30,1))

def predicted_dos_formula(a,b,delta):
    """
    Parameters
    ----------
    a : Elo rating of team a
    b : Elo rating of team b.
    delta : correction for HFA - not used for neutral sites or the COVID bubble

    Returns
    -------
    DoS : difference over sum estimate

    """
    DoS = -1 + 2/(1+exp((b-a-delta)/100))
    return DoS

season_year = 2019
analysis_list = season_query(season_year)


for g in analysis_list:
    #get previous elo ratings
    away_rating = season_elo_ratings_list[g[0]-1]
    home_rating = season_elo_ratings_list[g[2]-1]
    #get expected DoS value, compare it to the real one
    expected_dos = predicted_dos_formula(away_rating, home_rating, default_HFA)
    actual_dos = (g[1]-g[3])/(g[1]+g[3])
    dos_difference = actual_dos - expected_dos
    
    change_factor = default_K*dos_difference
    season_elo_ratings_list[g[0]-1] = season_elo_ratings_list[g[0]-1]+change_factor
    season_elo_ratings_list[g[2]-1] = season_elo_ratings_list[g[2]-1]-change_factor
    

print("Final set of Elo ratings after season "+str(season_year)+" presented below.")

print_list=[]

for i,r in enumerate(season_elo_ratings_list):
    rtg = int(r[0])
    team = team_abbreviation(i+1)
    print_list.append([rtg,team])
    
print_list = sorted(print_list,key=lambda x:-x[0])
pprint(print_list)
    