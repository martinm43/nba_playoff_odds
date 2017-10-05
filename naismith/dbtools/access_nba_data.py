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

def stringtime(epoch_time_num):
  return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time_num))

def epochtime_numeric_month(str_time):
  datetime_obj=datetime.datetime.strptime(str_time,"%m %d %Y")
  return time.mktime(datetime_obj.timetuple())

def epochdate_nba_api(str_time):
  datetime_obj=datetime.datetime.strptime(str_time,"%Y-%m-%d").strftime('%a %b %d %Y')
  return datetime_obj
  
def epochtime_nba_api(str_time):
  datetime_obj=datetime.datetime.strptime(str_time,"%Y-%m-%d")
  return time.mktime(datetime_obj.timetuple())

def games_query(start,end,datemode='off',source_table='bballref_scores'):
  db_dir=cwd+'/nba_data.sqlite'
  conn=sqlite3.connect(db_dir)
  c=conn.cursor()
  if source_table=='bballref_scores':
      if datemode=='off':
        str_input='SELECT away_team_id, away_pts, home_team_id, home_pts FROM bballref_scores\
                  WHERE datetime BETWEEN '+str(start)+' AND '+str(end)
      else:
        str_input='SELECT date,away_team_id, away_pts, home_team_id, home_pts FROM bballref_scores\
                  WHERE datetime BETWEEN '+str(start)+' AND '+str(end)
  elif source_table=='nba_py_api_data':
      if datemode=='off':
        str_input='SELECT away_standard_id, away_pts, home_standard_id, home_pts FROM nba_py_api_data\
                  WHERE (day_datetime BETWEEN '+str(start)+' AND '+str(end)+') AND (away_pts IS NOT NULL) AND (home_pts IS NOT NULL)'
      else:
        str_input='SELECT date,away_standard_id, away_pts, home_standard_id, home_pts FROM nba_py_api_data\
                  WHERE (day_datetime BETWEEN '+str(start)+' AND '+str(end)+') AND (away_pts IS NOT NULL) AND (home_pts IS NOT NULL)'
  games=c.execute(str_input).fetchall()
  return games

def teams_query():
  print(cwd+'/nba_data.sqlite')
  conn=sqlite3.connect(cwd+'/nba_data.sqlite')
  c=conn.cursor()
  str_input='SELECT bball_ref_id,abbreviation,conf_or_league FROM pro_api_teams'
  teams=c.execute(str_input).fetchall()
  pprint(teams)
  return teams

if __name__=='__main__':
  #Not yet tested
  start_input=raw_input('Please enter a start date, format May 6 2016')
  start_secs=epochtime(start_input)
  end_input=raw_input('Please enter an end date, format May 20, 2016')
  end_secs=epochtime(end_input)
  print(len(games_query(start_secs,end_secs,datemode='On')))
  
