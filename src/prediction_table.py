"""
Endfile for testing integration with the mcss.cpp shared library
Using the python library developed using C++ to rapidly speed up how standings are printed and presented
and allow for integration with more 'modern' interfaces -think flask or Django

"""

# Future import first

import argparse
from nba_database.nba_data_models import ProApiTeams as Team
from nba_database.queries import elo_ratings_list, epochtime
from datetime import datetime, timedelta

from pprint import pprint


def playoff_odds_calc(start_datetime, end_datetime, season_year, ratings_mode="Elo"):
    """

    Given a start, end, season_year, and a ratings calculation method
    with some other factors, determine the odds of every team of making
    the playoffs at any given time.

    Parameters
    ----------
    start_datetime : start of period to be used for analysis (Unix timestamp)
    end_datetime : end of period to be used for analysis (Unix timestamp)
    season_year : year that season nominally ends in
                (e.g. if season ends in 2021, use 2021)
    ratings_mode : Elo or SRS. Default mode is Elo.

    Returns
    -------
    a list of 2-item lists for each team (first item ATL, last item WAS)
    each list consists of [playoff odds,average wins]

    """

    from predict.cython_mcss.mcss_ext2 import simulations_result_vectorized
    from analytics.SRS import SRS
    from analytics.morey import SRS_regress, Elo_regress

    from nba_database.queries import games_query, games_won_query, future_games_query

    # Test results/inputs
    if end_datetime < start_datetime:
        print("Start date is after end date, please check inputs")
        return 1

    predict_date = end_datetime
    predict_season_year = season_year

    # Get List Of Known Wins
    games_list = games_query(start_datetime, end_datetime)
    games_won_list_cpp = games_won_query(games_list, return_format="matrix").tolist()

    # Get team data.
    teams_list = Team.select().order_by(Team.bball_ref)
    teams_list = [
        [x.bball_ref, x.team_name, x.abbreviation, x.division, x.conf_or_league]
        for x in teams_list
    ]


    #pprint(teams_list)
    # Division changes go here
    for z in teams_list:
        if season_year <= 2003 and z[0] == 19: #Charlotte Hornets to NOH change
            z[4]="E"
            z[3]="Central"

    #pprint("Fixed")
    #pprint(teams_list)



    # Get future games (away_team, home_team, home_team_win_probability)

    future_games_list = future_games_query(predict_date, predict_season_year)

    if ratings_mode == "SRS":
        # Get Team Ratings (and create Team object list)
        ratings_list = SRS(
            games_query(start_datetime, end_datetime)
        ).tolist()  # get ratings for that time.

        for i, x in enumerate(teams_list):
            x.append(ratings_list[i])
            for j in range(1, 5):  # "all strings"
                x[j] = x[j].encode("utf-8")

        for x in future_games_list:
            away_team_rating = teams_list[x[0] - 1][5]
            home_team_rating = teams_list[x[1] - 1][5]
            SRS_diff = home_team_rating - away_team_rating
            x.append(SRS_regress(SRS_diff))

    if ratings_mode == "Elo":
        ratings_list = elo_ratings_list(epochtime(end_datetime))
        for i, x in enumerate(teams_list):
            x.append(ratings_list[i])
            for j in range(1, 5):  # "all strings"
                x[j] = x[j].encode("utf-8")

        for x in future_games_list:
            away_team_rating = teams_list[x[0] - 1][5]
            home_team_rating = teams_list[x[1] - 1][5]
            Elo_diff = home_team_rating - away_team_rating
            x.append(Elo_regress(Elo_diff))

    team_results = simulations_result_vectorized(
        games_won_list_cpp, future_games_list, teams_list, season_year
    )
    # Return (top 8 odds, average wins, top 6 odds, and play in tournament odds).
    team_results = [
        [x[0] * 100.0, x[1], x[2] * 100.0, x[3] * 100.0] for x in team_results
    ]
    return team_results


def playoff_odds_print(team_results,season_year):
    """
    Prints table based on alphabetically ordered team results matrix.
    Team results are the output of playoff_odds_calc.
    """
    # Custom local function for formatting
    from tabulate import tabulate

    def format_percent(percent_float):
        return str(percent_float) + "%"

    # Format the results into a table
    teams = Team.select().order_by(Team.bball_ref)

    teams_dict = [
        dict(list(zip(["Team", "Conference"], [i.abbreviation, i.conf_or_league])))
        for i in teams
    ]


    for z in teams_dict:
        if z["Team"]=="NOP/NOH/CHA" and season_year <= 2003:
            z["Conference"]="E"


    for i, d in enumerate(teams_dict):
        d["Hist. Playoff %"] = round(team_results[i][0], 1)
        d["Avg. Wins"] = round(team_results[i][1], 1)
        d["Playoff %"] = round(team_results[i][2], 1)
        d["PIT %"] = round(team_results[i][3], 1)

        # Convert into percentages for printing
        d["Hist. Playoff %"] = format_percent(d["Hist. Playoff %"])
        d["Playoff %"] = format_percent(d["Playoff %"])
        d["PIT %"] = format_percent(d["PIT %"])

    teams_dict.sort(key=lambda x: (x["Conference"], -x["Avg. Wins"]))

    team_tuples = [
        (
            d["Conference"],
            d["Team"],
            d["Avg. Wins"],
            d["Hist. Playoff %"],
            d["PIT %"],
            d["Playoff %"],
        )
        for d in teams_dict
    ]

    results_table = tabulate(
        team_tuples,
        headers=[
            "Conference",
            "Team",
            "Avg. Wins",
            "Legacy Playoff Odds",
            "PIT Odds",
            "Post-2020 Playoff Odds",
        ],
        tablefmt="rst",
        numalign="left",
    )
    return results_table


# Print your results:

if __name__ == "__main__":

    season_year = 2024  # year in which season ends
    start_datetime = datetime(season_year - 1, 10, 10)  # start of season
    #end_datetime = datetime(season_year,4,30)  # a few weeks or months in
    end_datetime = datetime.today()-timedelta(days=1)

    parser = argparse.ArgumentParser(description='Process datetime-related arguments.')

    # Year argument
    parser.add_argument('--year', type=int, required=True, help='The year (e.g., 2023)')

    # Start datetime argument
    parser.add_argument('--start', type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                        required=True, help='Start datetime in the format YYYY-MM-DD')

    # End datetime argument
    parser.add_argument('--end', type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                        required=True, help='End datetime in the format YYYY-MM-DD')
    
    # Mode argument
    parser.add_argument('--mode', type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                        required=True, help='One of SRS or Elo')

    args = parser.parse_args()

    season_year = args.year
    start_datetime = args.start
    end_datetime = args.end
    ratings_mode = args.mode

    ratings_mode = args.mode
    results = playoff_odds_calc(
        args.start, args.end, args.year, ratings_mode=ratings_mode
    )
    results_table = playoff_odds_print(results,season_year)

    print(
        "Playoff odds for the "
        + str(season_year)
        + " season as of "
        + end_datetime.strftime("%b %d %Y")
    )
    print("Method used: " + ratings_mode)
    print(results_table)
    print(
        "Note that in 2014 and earlier, division winners were automatically given a top-four seed\n"
        + "and home court advantage for the first round. That logic has not yet been implemented in this progam"
    )


