# coding: utf-8
from datetime import datetime, timedelta
import pytz
from pprint import pprint

def day_dict_list(game_date):
    """
    Input a datetime object, return a dict containing a list of games played on that date.
    """
    from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2

    from nba_database.queries import epochtime, abbrev_to_id, id_to_name

    #s = ScoreboardV2(game_date = x_date)
    s = ScoreboardV2(game_date = game_date)

    day_results=s.line_score.get_dict()
    day_results_data=[dict(list(zip(day_results['headers'],x))) for x in day_results['data']]

    game_list=[]
    for i in range(0,len(day_results_data),2):
        away_team_data = day_results_data[i]
        home_team_data = day_results_data[i+1]

        game_dict={} #need to "rezero" before writing the dict.
        game_dict['away_pts'] = away_team_data['PTS']
        game_dict['away_team_id'] = abbrev_to_id(away_team_data['TEAM_ABBREVIATION'])
        game_dict['away_team'] = id_to_name(game_dict['away_team_id'])
        game_dict['home_pts'] = home_team_data['PTS']
        game_dict['home_team_id'] = abbrev_to_id(home_team_data['TEAM_ABBREVIATION'])
        game_dict['home_team'] = id_to_name(game_dict['home_team_id'])

        #This is required in order to deal with the 
        game_dict['datetime'] = epochtime(x_date)

        game_dict['date'] = x_date.strftime('%Y-%m-%d') 
        game_list.append(game_dict)

    return game_list

if __name__ == '__main__':
    import sys

    from nba_database.nba_data_models import BballrefScores

    start_date = datetime(2018,4,9,tzinfo=None)
    end_date = datetime(2018,4,12,tzinfo=None)
    x_date = start_date
    results = []
    
    while x_date <= end_date:
        print('Processing results for '+x_date.strftime('%Y-%m-%d'))
        partial_results = day_dict_list(x_date)
        for i in partial_results:
            results.append(i)
        x_date = x_date + timedelta(days=1)

    for game in results:
        pprint(game)
        BballrefScores.update(
            away_pts=game['away_pts'],
            home_pts=game['home_pts'],
            date=game['date']). where(
                game['date'] == BballrefScores.date,
                BballrefScores.away_team_id == game['away_team_id'],
                BballrefScores.home_team_id == game['home_team_id'],
                BballrefScores.season_year == 2019).execute()
