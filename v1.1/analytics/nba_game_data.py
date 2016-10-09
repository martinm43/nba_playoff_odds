#!/usr/bin/env python

#MAM - 5 May 2016

#Parsing data obtained from basketball-reference.com 
#for use in analyses. Your first Python program. 


#Replace Excel Program with Python routine.
import csv, os, time, datetime
import numpy as np
from pprint import pprint
from dbtools import create_db, col_creator, insert_data
from rest_and_travel import team_rest_calc, team_rest_calc_v2

#This is the best way that I can think of to convert the team names into the 1-30 numbers required for 
#calculating SRS. Here goes...
def teamind ( str ):
	if str=='Atlanta Hawks':
		return 1
	if str=='Boston Celtics':
		return 2
	if str=='Brooklyn Nets' or str=='New Jersey Nets':
		return 3
	if str=='Charlotte Hornets' or str=='Charlotte Bobcats':
		return 4 #Team renamed in 2014
	if str=='Chicago Bulls':
		return 5
	if str=='Cleveland Cavaliers':
		return 6
	if str=='Dallas Mavericks':
		return 7
	if str=='Denver Nuggets':
		return 8
	if str=='Detroit Pistons':
		return 9
	if str=='Golden State Warriors':
		return 10
	if str=='Houston Rockets':
		return 11
	if str=='Indiana Pacers':
		return 12
	if str=='Los Angeles Clippers':
		return 13
	if str=='Los Angeles Lakers':
		return 14
	if str=='Memphis Grizzlies' or str=='Vancouver Grizzlies':
		return 15
	if str=='Miami Heat':
		return 16
	if str=='Milwaukee Bucks':
		return 17
	if str=='Minnesota Timberwolves':
		return 18
	if (str=='New Orleans Pelicans' or str=='New Orleans Hornets' or str=='New Orleans/Oklahoma City Hornets'):
		return 19
	if str=='New York Knicks':
		return 20
	if str=='Oklahoma City Thunder' or str=='Seattle SuperSonics':
		return 21
	if str=='Orlando Magic':
		return 22
	if str=='Philadelphia 76ers':
		return 23
	if str=='Phoenix Suns':
		return 24
	if str=='Portland Trail Blazers':
		return 25
	if str=='Sacramento Kings':
		return 26
	if str=='San Antonio Spurs':
		return 27
	if str=='Toronto Raptors':
		return 28
	if str=='Utah Jazz':
		return 29
	if str=='Washington Wizards' or str=='Washington Bullets': #Retro!
		return 30
	else:
		return str

def season_to_dict(filename,year):
  #strings for getting to file locations 
  phone = ''

  ballrows = []
  with open(phone+filename,'rb') as csvfile:
     field_names=['date','start_time','box_score','away_team',\
                  'away_pts','home_team','home_pts','OT','Notes']
     balldata = csv.DictReader(csvfile,delimiter=',',fieldnames=field_names)
     csvfile.close
     for row in balldata: 
  	    ballrows.append(row)

  #clear blank entries
  ballrows=[row for row in ballrows if row['box_score']=='Box Score']

  #Convert names to IDs and add game id
  #based on year and change pts to integers
  game_id=year*10000+1
  
  for row in ballrows:
    row['id']=game_id
    row['away_team_id']=teamind(row['away_team'])
    row['home_team_id']=teamind(row['home_team'])
    row['home_pts']=int(row['home_pts'])
    row['away_pts']=int(row['away_pts'])
    
    #Seconds since epoch for rest-calculation purposes
    #earlier games around 2000 have no start times listed.
    if row['start_time']!='':
       row['datetime']=datetime.datetime.strptime(row['date'] + ' ' + row['start_time'],\
    	             '%a %b %d %Y %I:%M %p')
    else:
    		   row['datetime']=datetime.datetime.strptime(row['date'],\
    	             '%a %b %d %Y')
    row['datetime']=time.mktime(row['datetime'].timetuple())
    #add in year
    row['season_year']=year
    
    #print row['datetime']
    game_id+=1

  return ballrows

if __name__=='__main__':
  folder=''
  dbfile=folder+'nba_data_test.sqlite'
  new_table_name='bballref_scores'
  rest_table='bballref_rest'

  #create tables
  create_db(dbfile,new_table_name)
  create_db(dbfile,rest_table)

  #loop up
  start_year=1997
  end_year=2017  
  
  #For storing rest data
  set_rest_data=[]
  
  for year in range(start_year,end_year):
    season_file=folder+'leagues_NBA_'+str(year)+'_games_games.csv'
    season_games_list=season_to_dict(season_file,year)
    season_rest_list=team_rest_calc_v2(season_games_list)

    #only for the first year do we need to create columns
    if year==start_year:
      col_creator(dbfile,new_table_name,season_games_list[0])
      col_creator(dbfile,rest_table,season_rest_list[0])

    for game in season_games_list:
      print('Adding '+game['away_team']+' at '+game['home_team']+', '+game['date'])
      insert_data(dbfile,new_table_name,game)
    
    for game in season_rest_list:
      set_rest_data.append(game)
  
  #identify and write rest data
  i=1   
  for game in set_rest_data:
    game['id']=i
    print('Adding '+str(game['team_id'])+' rest data on '+'{}'.format(game['datetime']))
    insert_data(dbfile,rest_table,game)
    i+=1
