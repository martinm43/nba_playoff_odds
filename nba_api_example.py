# coding: utf-8
from datetime import datetime
from pprint import pprint

def day_dict_list(game_date):
    """
    Input a datetime object, return a dict containing a list of games played on that date.
    """
    from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2

    from nba_database.queries import epochtime, abbrev_to_id, id_to_name

    s = ScoreboardV2(game_date=x_date)

    day_results=s.line_score.get_dict()
    day_results_data=[dict(zip(day_results['headers'],x)) for x in day_results['data']]

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
        game_dict['datetime'] = epochtime(x_date)
        game_dict['date'] = x_date.strftime('%a %b %d %Y') 
        game_list.append(game_dict)

    return game_list

if __name__ == '__main__':
    from nba_database.nba_data_models import BballrefScores
    x_date = datetime(2018,10,17)
    results = day_dict_list(x_date)

    for game in results:
        pprint(game)
        BballrefScores.update(
            away_pts=game['away_pts'],
            home_pts=game['home_pts']). where(
                BballrefScores.datetime == game['datetime'],
                BballrefScores.away_team_id == game['away_team_id'],
                BballrefScores.home_team_id == game['home_team_id']).execute()
