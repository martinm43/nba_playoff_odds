"""
Endfile for testing integration with the mcss.cpp shared library
Using the python library developed using C++ to rapidly speed up how standings are printed and presented
and allow for integration with more 'modern' interfaces -think flask or Django
"""

from __future__ import print_function, division

from tabulate import tabulate
from mcss_ext2 import simulations_result_vectorized
from pprint import pprint
from mlb_data_models import Team, database

# define a "percentization function":


def format_percent(percent_float):
    return str(percent_float) + '%'


# get list of known wins
from supports import games_won_to_date, future_games_list
games_won_list_cpp = games_won_to_date(return_format="matrix").tolist()
fg_list_cpp = future_games_list()

# get the team rating data
query = database.execute_sql("select * from recent_ratings")
teams_list=[]
for q in query:
    team=[]
    team.append(int(q[0]))
    team.append(q[1])
    team.append(q[2])
    team.append(q[3])
    team.append(q[4])
    team.append(float(q[5]))
    teams_list.append(team)


team_results = simulations_result_vectorized(games_won_list_cpp, fg_list_cpp,teams_list)

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
