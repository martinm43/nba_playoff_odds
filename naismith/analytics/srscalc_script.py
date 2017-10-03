#SRS Calculations in Python
#See Doug Driner's definition of SRS as it applies in the NFL.
#This version is going to have straight calculations, nothing fancy.

#UPDATE Sep 2016: SVD approximation used to solve problem and avoid "blowing up"
from __future__ import division

#MAM
import sys
#print(sys.path)

#from .access_nba_data import epochtime, games_query 
import math
import csv
import numpy as np
import datetime
from pprint import pprint

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
    
    
  #Vector p.
  return np.divide(d,games)
  
#Warning: does not handle large or small lists of game data well
def srscalc(srsdata,calcmode='Numpy LS'):
  import os, csv
  wkdir = os.path.dirname(os.path.realpath(__file__))+'/'
  #define some variables for good practise but now, these are going to be arrays and matrices
  
  games=np.zeros(30)
  #Number of games played by each team.
  for i in range(1,31):
    games[i-1]=[sublist[2] for sublist in srsdata].count(i)+[sublist[0] for sublist in srsdata].count(i)
  
  #print(games)
  
  W=np.zeros((30,30))
    
  # The hard one - how do you calculate W? Have to use a loop. For each row increment the number
  # of each games played by each team in the weighting matrix by 1.
  for row in srsdata:
    W[int(row[2])-1][int(row[0])-1] += 1
    W[int(row[0])-1][int(row[2])-1] += 1

  
  #December 29 2016 Edit - Use Corrected Point Differentials
  #Raptors' sequence of absurd wins (45+ win over ATL, other 30+ wins) break
  #system to point where this kind of has to be done. - MAM
  #p=point_diff(srsdata)
  p=[]
  with open(wkdir+'adj_pts_diff_vector.csv','rb') as srsfile:
	rankdata = csv.reader(srsfile,delimiter=',')
	for row in rankdata:
		p.append(row)
	srsfile.close
  p=[float(x[0]) for x in p] #convert csv str into floats.
 
  # Divide W by the number of games played, similar to tested MATLAB code.
  W = np.divide(W,games)
  U = np.identity(30)-W

  #Solve and finish. Remember - this matrix is very close to singular
  #so inversion is not the way to solve it. The first entry out of the results matches
  #verified data so let's go with that
  
  #weird things happen if you dont do this - 
      #only so much resolution available
  #U=np.around(U,decimals=6)
  #p=np.around(p,decimals=6)
  
  
  #Calculation options.
  if calcmode=='Numpy LS':
    #handling old seasons by converting nans
    #practical but slow, can do better
    for i in range(0,len(p)):
      if math.isnan(p[i]):
        #print('NaN detected, corrected')
        p[i]=0
    
    for i in range(0,30):
      for j in range(0,30):
        if math.isnan(U[i,j]):
          U[i,j]=0
    #print U[0,:]
    #print p
    
    #print('SVD results follow')
    #Trying to use SVD as shown in https://codeandfootball.wordpress.com/2011/04/12/issues-with-the-simple-ranking-system/
    #To resolve singular issues. The idea is that we solve an approximation of the original system.
    
    svd_R1,svd_s,svd_R2=np.linalg.svd(U)
    
    tol=0.001
    svd_s.tolist()
    #print(svd_s)
    svd_s_inv=[d**(-1) for d in svd_s]
    svd_s_inv=np.asarray(svd_s_inv)
    #print(svd_s_inv)
    #SVD testing block
    #C=np.dot(svd_R1,np.dot(np.diag(svd_s),svd_R2))
    D=np.dot(svd_R1.transpose(),np.dot(np.diag(svd_s_inv),svd_R2.transpose()))
    X=np.dot(D,p)
    #print(C[0,:])
    #print('Product of svd_s gives a condition number '+str(np.prod(svd_s))) 
    #print(svd_s)
    
  srs_dict=[]
  srs_headers=['team_id','srs','point_diff']
  
  for i in range(0,30):
    game=dict(zip(srs_headers,[i+1,X[i],p[i]]))
    srs_dict.append(game)
  
  #print srs_dict
  return srs_dict

def srs_month_since_date(date, no_months=1): #date in "Seconds Since Epoch"
  month_secs=2592000 #30 days
  results=srscalc(games_query(date-month_secs*no_months,date))
  for srsdata in results:
    srsdata['calc_date']=int(date)
  return results

if __name__=='__main__':

    #Iterate through all of the season.
    #Get max dates and min dates then separate them
    #Get the srs calculation data (srsdata)
    start_secs=epochtime('Oct 1 2015')
    end_secs=epochtime('May 15 2016')
    gameslist=games_query(start_secs,end_secs)
    print(gameslist)
    print 'Number of games: '+str(len(gameslist))
    results=srscalc(gameslist)
    for game in results:
      game['start_date']=start_secs
      game['end_date']=end_secs
    pprint(results)
