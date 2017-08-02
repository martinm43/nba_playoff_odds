#-*-coding:utf8;-*-
#qpy:2
#qpy:console

#Choose working directory.
import os
cwd=os.getcwd()

import sqlite3
import time, datetime
from pprint import pprint

def epochtime(str_time):
  datetime_obj=datetime.datetime.strptime(str_time,"%b %d %Y")
  return time.mktime(datetime_obj.timetuple())
  
def epochtime_numeric_month(str_time):
  datetime_obj=datetime.datetime.strptime(str_time,"%m %d %Y")
  return time.mktime(datetime_obj.timetuple())

def epochdate_nba_api(str_time):
  datetime_obj=datetime.datetime.strptime(str_time,"%Y-%m-%d").strftime('%a %b %d %Y')
  return datetime_obj
  
def epochtime_nba_api(str_time):
  datetime_obj=datetime.datetime.strptime(str_time,"%Y-%m-%d")
  return time.mktime(datetime_obj.timetuple())

def games_query(start,end,datemode='off'):
  db_dir=cwd+'/nba_data_test.sqlite'
  conn=sqlite3.connect(db_dir)
  c=conn.cursor()
  if datemode=='off':
    str_input='SELECT away_team_id, away_pts, home_team_id, home_pts FROM bballref_scores\
              WHERE datetime BETWEEN '+str(start)+' AND '+str(end)
  else:
    str_input='SELECT date,away_team_id, away_pts, home_team_id, home_pts FROM bballref_scores\
              WHERE datetime BETWEEN '+str(start)+' AND '+str(end)
  games=c.execute(str_input).fetchall()
  return games

def teams_query():
  conn=sqlite3.connect(phone+'nba_data_test.sqlite')
  c=conn.cursor()
  if datemode=='off':
    str_input='SELECT bballref_team_id,abbreviation,conf_or_league FROM pro_api_teams'
  teams=c.execute(str_input).fetchall()
  pprint(teams)
  return teams

if __name__=='__main__':
  start_input=raw_input('Please enter a start date, format May 6 2016')
  start_secs=epochtime(start_input)
  end_input=raw_input('Please enter an end date, format May 20, 2016')
  end_secs=epochtime(end_input)
  print(len(games_query(start_secs,end_secs,datemode='On')))
  
