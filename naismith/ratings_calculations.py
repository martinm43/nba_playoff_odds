#19 December 2016
#The purpose of this script is to calculate onetime ratings of all the teams 
#that can then be used to calculate the binominal win probabilities for Monte 
#Carlo simulation.

#MAM

import csv,os
from analytics.srscalc_script import srscalc
from string_conversion_tools import team_abbreviation

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

import sqlite3
from dbtools.access_nba_data import epochtime
from pprint import pprint
tablename='nba_py_api_data'
filename='nba_data.sqlite'
conn=sqlite3.connect(wkdir+filename)
c=conn.cursor()

analysis_start_date=raw_input('Enter start date for Burke-type analysis (e.g. Jan 1 2016): ')
analysis_end_date=raw_input('Enter end date for Burke-type analysis (e.g. Feb 1 2016): ')
max_MOV=float(raw_input('Enter max margin of victory for Burke-type analysis: '))

analysis_start_date=epochtime(analysis_start_date)
analysis_end_date=epochtime(analysis_end_date)

nba_api_srsdata_query_str='SELECT away_standard_id, away_PTS, home_standard_id, home_PTS\
                             from nba_py_api_data WHERE day_datetime >= '+str(analysis_start_date)+' AND day_datetime <= '+str(analysis_end_date)
nba_api_srsdata=c.execute(nba_api_srsdata_query_str).fetchall()
srsdata=nba_api_srsdata

###END OF V2.0 EDITS ###################################################

#Convert the data into integers (this will not be necessary if using DB data)
srsdata=[[int(m) for m in l] for l in srsdata]

if burke_solve==1:
    #Calculate Burke SRS
    burke_data=[[s[2],s[0],s[3],s[1]] for s in srsdata]
    burkelist=burke_calc(burke_data,impmode=None,max_MOV=max_MOV,home_team_adv=2.0)
    burkelist=[[b] for b in burkelist]
else:
    burkelist=None
#Debug
print('Printing Burke Ratings:')
if burkelist!=None:
  for i, burke_value in enumerate(burkelist):
      print('Burke rating of team '+team_abbreviation(i+1)+' is '+str(burke_value[0]))
else:
  print('Burke calculations not performed, skipping')
#Print results to screen
print('\n')

#SRS_vector for writing to file
SRS_vector=[[s['srs']] for s in srsdicts]
#print SRS_vector

#write it out.
csvfile_out = open(wkdir+'SRS_vector.csv','wb')
csvwriter = csv.writer(csvfile_out)
for row in SRS_vector:
	#Only need to print the visiting and home team scores and names.
	csvwriter.writerow(row)
csvfile_out.close()

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

