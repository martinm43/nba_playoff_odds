"""
Short sample script that plots the moving elo for a given team over their 
available history in the Elo database.
-- Martin
"""

import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from random import randint
from datetime import datetime, timedelta

from nba_database.queries import team_abbreviation

team_id = randint(1,31)

conn = sqlite3.connect('nba_data.sqlite')
query = "SELECT datetime,elo_rating FROM nba_team_elo_data where team_id = "+\
    str(team_id)

df = pd.read_sql_query(query,conn)

df['datetime'] = pd.to_datetime(df['datetime'],unit='s')

#get the appropriate colours
cursor = conn.cursor()
cursor.execute("SELECT primary_color from pro_api_teams where bball_ref_id="+str(team_id))
s = cursor.fetchall()


plt.plot(df['datetime'],df['elo_rating'].rolling(41).mean(),\
         label= '41 game moving avg.',color=s[0][0])
plt.xticks(rotation=45)
plt.legend()
plt.title("Elo rating history of "+team_abbreviation(team_id)+", 1996-2020")
plt.show()
