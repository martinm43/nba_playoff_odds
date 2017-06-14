#-*-coding:utf8;-*-
#qpy:2
#qpy:console

app_dir='/home/martin/naismith/'
phone=app_dir+'v1.0_dev/db_folder/'

import sqlite3
import time, datetime
from pprint import pprint

def epochtime(str_time):
  datetime_obj=datetime.datetime.strptime(str_time,"%b %d %Y")
  return time.mktime(datetime_obj.timetuple())
  
def games_query(start,end,datemode='off'):
  phone='/home/martin/Documents/naismith/v1.1/nba_db_folder/'
  conn=sqlite3.connect(phone+'nba_data_test.sqlite')
  c=conn.cursor()
  if datemode=='off':
    str_input='SELECT away_team_id, away_pts, home_team_id, home_pts FROM bballref_scores\
              WHERE datetime BETWEEN '+str(start)+' AND '+str(end)
  else:
    str_input='SELECT date,away_team_id, away_pts, home_team_id, home_pts FROM bballref_scores\
              WHERE datetime BETWEEN '+str(start)+' AND '+str(end)
  games=c.execute(str_input).fetchall()
  pprint(games)
  return games

if __name__=='__main__':
  start_input=raw_input('Please enter a start date, format May 6 2016')
  start_secs=epochtime(start_input)
  end_input=raw_input('Please enter an end date, format May 20, 2016')
  end_secs=epochtime(end_input)
  print(len(games_query(start_secs,end_secs,datemode='On')))
  
