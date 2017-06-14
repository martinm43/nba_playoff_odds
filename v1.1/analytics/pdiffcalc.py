#SRS Calculations in Python
#See Doug Driner's definition of SRS as it applies in the NFL.
#This version is going to have straight calculations, nothing fancy.

#MAM
app_dir='/home/martin/naismith/'

#Regular modules
from season_dates import get_start_date,get_end_date
import math
import csv
import numpy as np
import datetime
from pprint import pprint
#Analytics modules (in folder)
from access_nba_data import epochtime, games_query 

import sys
sys.path.append(app_dir+'v1.0_dev/python_db_tools/')
from dbtools import create_db, col_creator, insert_data

#the big guns - solution options using bigger fancier packages
try:
  import sympy
  from scipy.sparse.linalg import lsqr, spsolve
  from scipy.sparse import csc_matrix
except:
  print('One or more advanced analytics modules not found')

#define a function for converting those strings into indices:
def str_ind (str):
	return int(str)-1

def point_diff(srsdata):
  d=np.zeros(30)
  games=np.zeros(30)
  #Number of games played by each team.
  for i in range(1,31):
    games[i-1]=[sublist[2] for sublist in srsdata].count(i)+[sublist[0] for sublist in srsdata].count(i)
  #Calculate point differential for all games involving a team (home and away) for each team.
  for i in range(1,31):
    a = [float(sublist[3])-float(sublist[1]) for sublist in srsdata if int(sublist[2]) == i]
    b = [float(sublist[1])-float(sublist[3]) for sublist in srsdata if int(sublist[0]) == i]
    d[i-1]=sum(a)+sum(b)

  for g in games:
    g=float(g)
    if g==0:
      print('Correcting zero games entry')
      g=1
      
  #Vector p.
  p=np.divide(d,games)
  p.tolist()
  
  p_dict=[]
  p_headers=['team_id','point_diff']
  
  for i in range(0,30):
    p_set=dict(zip(p_headers,[i+1,p[i]]))
    p_dict.append(p_set)
    
  return p_dict
 
def p_month_since_date(date): #date in "Seconds Since Epoch" 
  results=point_diff(games_query(date-2592000,date))
  for pdata in results:
    pdata['calc_date']=int(date)
  return results
 
if __name__=='__main__':

    #db
    db_folder=app_dir+'v1.0_dev/db_folder/'
    dbfile=db_folder+'nba_data_test.sqlite'
    tablename='pointdiff'
    create_db(dbfile,tablename)

    #Iterate through all of the season.
    #Get max dates and min dates then separate them
    #Get the srs calculation data (srsdata)
    start_secs=epochtime('Oct 15 2015')
    end_secs=epochtime('Apr 20 2016')
    gameslist=games_query(start_secs,end_secs)
    print len(gameslist)
    results=point_diff(gameslist)
    for game in results:
      game['start_date']=start_secs
      game['end_date']=end_secs
    pprint(results)
    
    col_creator(dbfile,tablename,results[0])
    
    i=1
    for game in results:
      game['id']=i
      insert_data(dbfile,tablename,game)
      i+=1
      
    print datetime.datetime.today()
    
    
    # srs_results=[item for sublist in srs_results for item in sublist]
    #pprint(srs_results)
    # #trivial conversion to dict
    # team_id_array=[]
    # for i in range(1,31):
      # team_id_array.append('Team '+str(i))
    # srs_dict=dict(zip(team_id_array,srs_results))
    # print(sorted(srs_dict.values()))
    
   
