"""
Ratings_Calculations

This script calculates the Burke ratings for NBA teams over a given time period with a given 
maximum/minimum margin of victory and average home team advantage for use in the projections
scripts. 

Automation requirements

Human input: Automatic input

Start date for analysis: 6 weeks before
End date for analysis: current date
Maximum margin of victory: 15
Average home court advantage: 2

"""

import csv,os
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

tablename='nba_py_api_data'
filename='nba_data.sqlite'
conn=sqlite3.connect(wkdir+filename)
c=conn.cursor()



###END OF V2.0 EDITS ###################################################

#Convert the data into integers (this will not be necessary if using DB data)
srsdata=[[int(m) for m in l] for l in srsdata]

if burke_solve==1:
    #Calculate Burke SRS
    analysis_start_date=raw_input('Enter start date for Burke-type analysis (e.g. Jan 1 2016): ')
    analysis_end_date=raw_input('Enter end date for Burke-type analysis (e.g. Feb 1 2016): ')
    max_MOV=float(raw_input('Enter max margin of victory for Burke-type analysis: '))
    home_team_adv=float(raw_input('Enter presumed home team advantage: '))
    analysis_start_date=epochtime(analysis_start_date)
    analysis_end_date=epochtime(analysis_end_date)
    nba_api_srsdata_query_str='SELECT away_standard_id, away_PTS, home_standard_id, home_PTS\
                             from nba_py_api_data WHERE day_datetime >= '+str(analysis_start_date)+' AND day_datetime <= '+str(analysis_end_date)
    nba_api_srsdata=c.execute(nba_api_srsdata_query_str).fetchall()
    srsdata=nba_api_srsdata
    burke_data=[[s[2],s[0],s[3],s[1]] for s in srsdata if s[1] is not None]
    burkelist=burke_calc(burke_data,impmode=None,max_MOV=max_MOV,home_team_adv=home_team_adv)
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
