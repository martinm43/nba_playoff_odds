# coding: utf-8

# %load ORM_rest_calculation.py
from dbtools.rest_and_travel import team_rest_calc_v2
from dbtools.nba_data_models import BballrefScores, BballrefRest,database
from dbtools.max_sql_variables import max_sql_variables
import sqlite3

def ORM_bballref_rest_calc(calc_season_year):

    g=BballrefScores.select().where(BballrefScores.season_year==calc_season_year)
    g_dicts=g.dicts()
    rest_dicts=team_rest_calc_v2(g_dicts,calc_season_year)
    rest_dicts[0]

    #incidental type conversions
    for r in rest_dicts:
        r['team']=int(r['team_id'])
        r['game']=int(r['game_id'])
        del r['team_id']
        del r['game_id']

    #print(rest_dicts[0].keys())
    
    SQLITE_MAX_VARIABLE_NUMBER=max_sql_variables()
    
    with database.atomic() as txn:
        size = (SQLITE_MAX_VARIABLE_NUMBER // len(rest_dicts[0])) - 1 
        # remove one to avoid issue if peewee adds some variable
        for i in range(0, len(rest_dicts), size):BballrefRest.insert_many(rest_dicts[i:i+size]).upsert().execute()
  
    return 1

if __name__=='__main__':
    ORM_bballref_rest_calc(2018)