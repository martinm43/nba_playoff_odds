# coding: utf-8

"""

Brief script for processing the raw lists of schedules
provided by fixturedownload.com. If you use that site please
donate to them: they make parsing data easy!

Inputs: A schedule file.
Headers are as follows:
Round Number,Date,Location,Home Team,Away Team,Result
-- Note that the website uses "LA Clippers" not "Los Angeles Clippers"

Outputs:
    None, writes to the database as blank "games to be played"

"""

import pandas as pd
from datetime import datetime

from nba_database.queries import epochtime, full_name_to_id
from nba_database.nba_data_models import database, BballrefScores

SQLITE_MAX_VARIABLE_NUMBER = 100

#Please make sure to donate to 
df = pd.read_csv("nba-2020-EasternStandardTime.csv")

season_dicts = df.T.to_dict().values()

season_year = 2021
entry_id=1
for d in season_dicts:
    d['home_team'] = d['Home Team']
    d.pop("Home Team", None)
    d['home_team_id'] = full_name_to_id(d['home_team'])
    
    d['away_team'] = d['Away Team']
    d.pop("Away Team", None)
    d['away_team_id'] = full_name_to_id(d['away_team'])
    
    datestr = d['Date']
    d['date'] = d['Date']
    datefmt = '%d/%m/%Y %H:%M'
    date_datetime = datetime.strptime(datestr,datefmt)
    d['datetime'] = epochtime(date_datetime)
    
    d['season_year'] = season_year
    
    d.pop("Round Number",None)
    d.pop("Location",None)
    d.pop("Result",None)
    d.pop("Date",None)
    
    d['id'] = season_year*10000 + entry_id
    entry_id+=1
    

BballrefScores.insert_many(season_dicts).on_conflict_replace().execute()