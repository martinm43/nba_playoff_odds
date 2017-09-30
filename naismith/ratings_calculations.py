#19 December 2016
#The purpose of this script is to calculate onetime ratings of all the teams 
#that can then be used to calculate the binominal win probabilities for Monte 
#Carlo simulation.

#MAM

import csv,os
from analytics.srscalc_script import srscalc

#print(srscalc)

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

###BEGINNING OF V2.0 EDITS #############################################
#Obtaining data from the nba_py_api_data table - v1.4 edit

#Old method, no longer used.
#print('Calculating models')
#target='outfile_gms.csv'
#  
#with open(wkdir+target,'rb') as csvfile:
#	balldata = csv.reader(csvfile,delimiter=',')
#	for row in balldata:
#		srsdata.append(row)
#csvfile.close

import sqlite3
from dbtools.access_nba_data import epochtime
from pprint import pprint
tablename='nba_py_api_data'
filename='nba_data.sqlite'
conn=sqlite3.connect(wkdir+filename)
c=conn.cursor()

#analysis_start_date=raw_input('Enter start date for analysis (e.g. Jan 1 2016): ')
#analysis_end_date=raw_input('Enter end date for analysis (e.g. Feb 1 2016): ')
analysis_start_date='Nov 1 2016'
analysis_end_date='Dec 25 2016'

analysis_start_date=epochtime(analysis_start_date)
analysis_end_date=epochtime(analysis_end_date)

nba_api_srsdata_query_str='SELECT away_standard_id, away_PTS, home_standard_id, home_PTS\
                             from nba_py_api_data WHERE day_datetime >= '+str(analysis_start_date)+' AND day_datetime <= '+str(analysis_end_date)
nba_api_srsdata=c.execute(nba_api_srsdata_query_str).fetchall()
srsdata=nba_api_srsdata

###END OF V2.0 EDITS ###################################################

#Convert the data into integers (this will not be necessary if using DB data)
srsdata=[[int(m) for m in l] for l in srsdata]

#Calculate SRS via blow-up proof approximation.
srsdicts=srscalc(srsdata)

if burke_solve==1:
    #Calculate Burke SRS
    burke_data=[[s[2],s[0],s[3],s[1]] for s in srsdata]
    burkelist=burke_calc(burke_data,impmode=None)
    burkelist=[[b] for b in burkelist]

#Print results to screen
print('Calculated SRS results via SVD:')
for s in srsdicts:
  print('Team '+str(s['team_id'])+', SRS (SVD approx): '+str(s['srs']))

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
