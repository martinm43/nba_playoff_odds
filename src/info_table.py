"""

A script that produces a table of information. Inputs below.
-- start date
-- end date
-- season year (denoted by end)

Output: table (string)

"""
# Standard imports
from datetime import datetime, timedelta
import sys
import argparse
from pprint import pprint 

# Third Party Imports
from tabulate import tabulate

# Query imports
from nba_database.queries import (
    games_query,
    team_abbreviation,
    epochtime,
    elo_ratings_list,
    form_query,
    new_srs_ratings_list
)
from nba_database.nba_data_models import BballrefScores as Game
from analytics.wins_script import get_wins
from analytics.pythag import league_pythagorean_wins
from analytics.SRS import SRS
"""
parser = argparse.ArgumentParser(description='Process datetime-related arguments.')

#Year argument
parser.add_argument('--year', type=int, required=True, help='The year (e.g., 2023)')

# Start datetime argument
parser.add_argument('--start', type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                    required=True, help='Start datetime in the format YYYY-MM-DD')

# End datetime argument
parser.add_argument('--end', type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                    required=True, help='End datetime in the format YYYY-MM-DD')

args = parser.parse_args()

season_year = args.year
start_datetime = args.start
end_datetime = args.end
"""
season_year=2024
#start_datetime=datetime.today()-timedelta(days=60)
start_datetime=datetime(2023,10,1)
end_datetime=datetime.today()-timedelta(days=1)
games_list = games_query(start_datetime,end_datetime)

# Custom SRS calculation options
max_MOV = 100  # no real max MOV
home_team_adv = 0
win_floor = 0

wins_dict_list = [
    get_wins(i, season_year, start_datetime, end_datetime) for i in range(1, 31)
]
wins_list = [[x["away_record"], x["home_record"], x["record"]] for x in wins_dict_list]

win_pct_list = []
for x in wins_dict_list:
    wins,losses = map(int,x['record'].split('-'))
    winpct = wins/(wins+losses)
    win_pct_list.append(winpct)


# Pythagorean Wins
lpw_results = league_pythagorean_wins(
    Game,
    mincalcdatetime=epochtime(start_datetime),
    maxcalcdatetime=epochtime(end_datetime),
)

srs_list = new_srs_ratings_list(epochtime(end_datetime))

elo_list = elo_ratings_list(epochtime(end_datetime))

form_list = [form_query(i) for i in range(1, 31)]

lpw_results.sort(key=lambda x: x[0])

results = list(zip(lpw_results, srs_list, wins_list, elo_list, form_list,win_pct_list))

results = [
    [x[0][0], x[0][1], x[1], x[2][0], x[2][1], x[2][2], x[3], x[4],x[5]] for x in results
]

results_tuples = [
    (
        team_abbreviation(x[0]),
        round(x[1], 0),
        round(x[2] * 100.0 / 100.0, 3),
        x[6],
        x[3],
        x[4],
        x[5],
        x[7],
        round(x[8]*100.0/100.0,3)
    )
    for x in results
]

results_tuples.sort(key=lambda x: -x[2])

results_table = tabulate(
    results_tuples,
    headers=[
        "Team",
        "Pythag. Wins",
        "Est. SRS",
        "Elo Rating",
        "Away Record",
        "Home Record",
        "Overall Record",
        "Form",
        "Win %"
    ],
    tablefmt="rst",
    numalign="left",
)

print(
    "Pythagorean Win Expectations, Est. SRS, Elo, and Records \n"
    + "Based on Games Played Between: "
    + start_datetime.strftime("%b %d %Y")
    + " and "
    + end_datetime.strftime("%b %d %Y")
)
print(results_table)
