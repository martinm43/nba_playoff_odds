"""
Endfile for testing integration with the mcss.cpp shared library
Using the python library developed using C++ to rapidly speed up how standings are printed and presented
and allow for integration with more 'modern' interfaces -think flask or Django

"""

#Future import first
from __future__ import print_function, division
#Standard imports
from pprint import pprint
from datetime import datetime
#Third party imports
from tabulate import tabulate
#Library imports
from predict.cython_mcss.mcss_ext2 import simulations_result_vectorized
from analytics.SRS import SRS
from analytics.morey import SRS_regress
from nba_database.nba_data_models import ProApiTeams as Team
from nba_database.nba_data_models import database
from nba_database.queries import games_query, games_won_query, future_games_query
#Custom local function for formatting
def format_percent(percent_float):
    return str(percent_float) + '%'

#Set parameters for analysis
start_datetime = datetime(2015,10,1)
end_datetime = datetime(2016,03,1)
season_year = 2016

# Get List Of Known Wins
games_list = games_query(start_datetime,end_datetime)
games_won_list_cpp = games_won_query(games_list,return_format="matrix").tolist()

# Get Team Ratings (and create Team object list)
ratings_list=SRS(games_query(start_datetime,end_datetime)).tolist() #get ratings for that time.
teams_list=Team.select().order_by(Team.bball_ref)
teams_list=[[x.bball_ref, x.team_name, x.abbreviation,\
                    x.division, x.conf_or_league] for x in teams_list]
for i, x in enumerate(teams_list):
    x.append(ratings_list[i])
pprint(teams_list)

#Get future games (away_team, home_team, home_team_win_probability)
future_games_list = future_games_query(end_datetime, 2016)
for x in future_games_list:
    away_team_rating=teams_list[x[0]-1][5]
    home_team_rating=teams_list[x[1]-1][5]
    SRS_diff=home_team_rating-away_team_rating
    x.append(SRS_regress(SRS_diff))
pprint(future_games_list)

"""
teams = Team.select()

teams_dict = [
    dict(zip(['Team', 'Division'], [i.mlbgames_name, i.division])) for i in teams]
for i, d in enumerate(teams_dict):
    d['Win Division'] = round(team_results[i][0] * 100.0, 1)
    d['Win Wild Card'] = round(team_results[i][1] * 100.0, 1)
    d['Avg. Wins'] = round(team_results[i][2], 1)
    d['Make Playoffs'] = d['Win Division'] + d['Win Wild Card']
    # Convert into percentages for printing
    d['Win Division'] = format_percent(d['Win Division'])
    d['Win Wild Card'] = format_percent(d['Win Wild Card'])
    d['Make Playoffs'] = format_percent(d['Make Playoffs'])

teams_dict.sort(key=lambda x: (x['Division'], -x['Avg. Wins']))

team_tuples = [
    (d['Division'],
     d['Team'],
     d['Avg. Wins'],
     d['Win Division'],
     d['Win Wild Card'],
     d['Make Playoffs']) for d in teams_dict]

results_table = tabulate(
    team_tuples,
    headers=[
        'Division',
        'Team',
        'Avg. Wins',
        'Win Division',
        'Win Wild Card',
        'Make Playoffs'],
    tablefmt='rst',
    numalign='left')

print(results_table)
"""
