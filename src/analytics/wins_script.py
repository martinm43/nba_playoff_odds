# coding: utf-8
def get_wins(team_id,season_year,start_datetime,end_datetime):
    from nba_database.nba_data_models import BballrefScores as BS
    from nba_database.queries import team_abbreviation, epochtime
    away_query = BS.select().where(BS.season_year == season_year,\
                          BS.away_team_id == team_id,\
                          BS.away_pts > 0,\
                          BS.datetime >= epochtime(start_datetime),\
                          BS.datetime <= epochtime(end_datetime))
    away_results = [[i.away_pts, i.home_pts] for i in away_query]
    away_wins_total = sum([1 if x[0] > x[1] else 0 for x in away_results])
    away_games_total = len(away_results)
    #home_query = BS.select().where(BS.season_year == season_year, BS.home_team_id == team_id, BS.home_pts > 0)
    home_query = BS.select().where(BS.season_year == season_year,\
                          BS.home_team_id == team_id,\
                          BS.away_pts > 0,\
                          BS.datetime >= epochtime(start_datetime),\
                          BS.datetime <= epochtime(end_datetime))
    home_results = [[i.home_pts, i.away_pts] for i in home_query]
    home_wins_total = sum([1 if x[0] > x[1] else 0 for x in home_results])
    home_games_total = len(home_results)
    
    away_record = str(away_wins_total)+'-'+str(away_games_total-away_wins_total)
    home_record = str(home_wins_total)+'-'+str(home_games_total-home_wins_total)
    record = str(away_wins_total+home_wins_total)+'-'+str(away_games_total+home_games_total-away_wins_total-home_wins_total)

    return {'away_record':away_record,'home_record':home_record,'record':record}

