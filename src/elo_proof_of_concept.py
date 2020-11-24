
from nba_database.queries import season_query, team_abbreviation
from pprint import pprint
from math import exp
from random import randint
import numpy as np


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


def season_elo_calc(_analysis_list,previous_ratings=None,new_season=True):
    
    default_rating = 0.01 #1 gives good results.
    rating_scaling = 10 #10 gives good spread
    default_K = default_rating/rating_scaling

    if new_season == True:
        season_elo_ratings_list = default_rating*np.ones((30,1))
    else:
        season_elo_ratings_list = previous_ratings
        
    for g in _analysis_list:

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

    return season_elo_ratings_list

def year_to_year_ratings(season_elo_ratings_list,reset_factor=0.25,reset_value=0.01):
    previous_ratings = np.array(season_elo_ratings_list)
    #print(previous_ratings)
    new_ratings = previous_ratings*(1-reset_factor)+reset_factor*reset_value*np.ones((30,1))
    new_ratings.tolist()
    new_ratings = [r for r in new_ratings]
    return new_ratings

def results_summary(season_elo_ratings_list, scaling = 100000):
    
    print_list = []
    
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
    spread = print_list[0][0]-print_list[29][0]
    spread_string = "%.1f" % spread
    print("Max spread is: "+spread_string)
    
    return 

if __name__ == "__main__":

    start_year = 1999
    end_year = 2021
    reset_factor = .25 #1: every season is new. #0: every season is a continuation
    reset_value = 0.01 #identical to default value
    for season_year in range(start_year,end_year):
    
        if season_year == start_year:
            analysis_list = season_query(season_year)
            season_elo_ratings_list = season_elo_calc(analysis_list)
            results_summary(season_elo_ratings_list)
        else:
            analysis_list = season_query(season_year)
            season_elo_ratings_list = season_elo_calc(analysis_list,season_elo_ratings_list,new_season=False)
            results_summary(season_elo_ratings_list)
        season_elo_ratings_list = year_to_year_ratings(season_elo_ratings_list,reset_factor=reset_factor,reset_value=reset_value)
        