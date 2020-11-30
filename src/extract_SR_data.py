# For parsing .csv files obtained from the Sports-Reference website.
# All data belongs to Sports Reference LLC themselves.
from pprint import pprint
import pandas as pd
from datetime import datetime

from nba_database.queries import epochtime, full_name_to_id
from nba_database.nba_data_models import database, BballrefScores

season_year = 1991
df = pd.read_csv('season_data_91-92.csv')
season_dicts = df.T.to_dict().values()

print(len(season_dicts))

SQLITE_MAX_VARIABLE_NUMBER = 100

id = 1
for d in season_dicts:

    #pprint(d)
    d['home_team'] = d['Home/Neutral']
    d['away_team'] = d['Visitor/Neutral']
    d['home_pts'] = d['Home_PTS']
    d['away_pts'] = d['Visitor_PTS']
    d['home_team_id'] = full_name_to_id(d['Home/Neutral'])
    d['away_team_id'] = full_name_to_id(d['Visitor/Neutral'])
    d['date'] = d['Date']
    d['season_year'] = season_year+1
    #d['start_time'] = d['Start (ET)'] -- newer seasons only

    #date conversion - newer seasons
    #datestr = d['Date'] + ' ' + d['Start (ET)']+ 'm'
    #datefmt = '%a %b %d %Y %H:%M%p'
    #date conversion - older seasons
    datestr = d['Date']
    datefmt = '%a %b %d %Y'
    date_datetime = datetime.strptime(datestr,datefmt)
    d['datetime'] = epochtime(date_datetime)


    d.pop('Visitor/Neutral',None)
    d.pop('Home/Neutral',None)
    d.pop('Attend.',None)
    d.pop('x1',None)
    d.pop('x2',None)
    d.pop('Home_PTS',None)
    d.pop('Visitor_PTS',None)
    d.pop('Notes',None)
    d.pop('Start (ET)',None)
    d.pop('Date',None)
    d.pop('Unnamed: 5',None)
    d.pop('Unnamed: 6',None)
    d.pop('Unnamed: 7',None)

    d['id'] = season_year*10000 + id
    id+=1

season_dicts = list(season_dicts)
pprint(season_dicts[0])

with database.atomic() as txn:
     size = (SQLITE_MAX_VARIABLE_NUMBER // len(season_dicts[0])) - 1 
     # remove one to avoid issue if peewee adds some variable
     for i in range(0, len(season_dicts), size):
        BballrefScores.insert_many(season_dicts[i:i+size]).on_conflict_replace().execute()
  
