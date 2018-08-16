# coding: utf-8
def burke_month_calc(calcdate):
    from dbtools.nba_data_models import BballrefScores
    from analytics.burke_solver import burke_calc
    month_in_secs=60*60*24*30
    s=BballrefScores.select().where(BballrefScores.datetime<=calcdate,BballrefScores.datetime>=calcdate-month_in_secs)
    games=[(i.away_team_id,i.away_pts,i.home_team_id,i.home_pts) for i in s]
    return burke_calc(games)
