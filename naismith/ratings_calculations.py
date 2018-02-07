"""
Ratings_Calculations

This script calculates the Burke ratings for NBA teams over a given time period with a given 
maximum/minimum margin of victory and average home team advantage for use in the projections
scripts. 

Automation requirements

Human input: Automatic input

End date for analysis: current date
Maximum margin of victory: 15
Average home court advantage: 2

"""

import csv,os
import time
from string_conversion_tools import team_abbreviation
import sqlite3
from dbtools.access_nba_data import epochtime

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

#Handling Burke solver's dependence on scipy.
burke_solve=0
try:
    import scipy.optimize
    from analytics.burke_solver import burke_calc
    burke_solve=1
except ImportError:
    print('Burke solution method not available')
    
    


srsdata=[]

filename='nba_data.sqlite'
conn=sqlite3.connect(wkdir+filename)
c=conn.cursor()



###END OF V2.0 EDITS ###################################################

#Convert the data into integers (this will not be necessary if using DB data)
srsdata=[[int(m) for m in l] for l in srsdata]

if burke_solve==1:
    #Calculate Burke SRS
    
    #New automated code.
    analysis_start_date=time.time()-12*7*86400 #N weeks*days*seconds
    analysis_end_date=time.time()
    max_MOV=20.0
    home_team_adv=2.0

    nba_api_srsdata_query_str='SELECT away_team_id, away_PTS, home_team_id, home_PTS\
                             from bballref_scores WHERE datetime >= '+str(analysis_start_date)+' AND datetime <= '+str(analysis_end_date)
    nba_api_srsdata=c.execute(nba_api_srsdata_query_str).fetchall()
    srsdata=nba_api_srsdata
    burke_data=[[s[2],s[0],s[3],s[1]] for s in srsdata if s[1] is not None]
    burkelist=burke_calc(burke_data,impmode=None,max_MOV=max_MOV,home_team_adv=home_team_adv,win_floor=6.0)
    burkelist=[[b] for b in burkelist]
else:
    burkelist=None
#Debug
print('Printing Burke Ratings.')
if burkelist!=None:
  for i, burke_value in enumerate(burkelist):
      print('Burke rating of team '+team_abbreviation(i+1)+' is '+str(burke_value[0]))
else:
  print('Burke calculations not performed, skipping')

if burke_solve==1:
    #write out burke vector
    csvfile_out = open(wkdir+'burke_vector.csv','wb')
    csvwriter = csv.writer(csvfile_out)
    for row in burkelist:
        #Only need to print the visiting and home team scores and names.
        csvwriter.writerow(row)
    csvfile_out.close()


#### Close connection ####
conn.close()
