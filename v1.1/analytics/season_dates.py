#-*-coding:utf8;-*-
#qpy:2
#qpy:console

def get_end_date(year):
  phone='/storage/emulated/0/download/'

  import sqlite3
  from pprint import pprint

  conn=sqlite3.connect(phone+'nba_data_test.sqlite')
  c=conn.cursor()

  str_input='SELECT max(datetime) FROM bballref_scores\
             WHERE season_year='+str(year)
  
  result=c.execute(str_input).fetchall()

  print 'End date'
  print result
  return result[0][0]

def get_start_date(year):
  phone='/storage/emulated/0/download/'

  import sqlite3
  from pprint import pprint

  conn=sqlite3.connect(phone+'nba_data_test.sqlite')
  c=conn.cursor()

  str_input='SELECT min(datetime) FROM bballref_scores\
             WHERE season_year='+str(year)
  
  result=c.execute(str_input).fetchall()

  return result[0][0]

def srs_analysis():
  phone='/storage/emulated/0/download/'

  import sqlite3
  from pprint import pprint

  conn=sqlite3.connect(phone+'nba_data_test.sqlite')
  c=conn.cursor()

  str_input='SELECT srs1.srs,bballref_scores.away_pts\
             FROM bballref_scores\
             LEFT JOIN srs_table as srs1 ON\
             (srs1.team_id=bballref_scores.away_team_id AND srs1.calc_date=bballref_scores.datetime)'
  
  result=c.execute(str_input).fetchall()


  conn.close()
  #print type(result[0][0])
  return result


if __name__=='__main__':
  #print get_start_date(2016)
  #print get_end_date(2016)
  print srs_analysis()