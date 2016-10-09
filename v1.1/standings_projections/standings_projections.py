#MAM - 16 Jan 16 

#Parsing data obtained from basketball-reference.com 
#for use in analyses. Your first Python program. 


#Replace Excel Program with Python routine.
import sqlite3
#from pprint import pprint

#CSV output function
#Part Two: Write out a file containing all games played
def list_to_csv(csvfile,list_of_lists):
    import csv
    csvfile_out = open(csvfile,'wb')
    csvwriter = csv.writer(csvfile_out)
    for row in list_of_lists:
        #Only need to print the visiting and home team scores and names.
        csvwriter.writerow(row)
    csvfile_out.close()
    return 1

#get the conversion function
import sys
sys.path.append('/home/martin/naismith/v1.1/analytics/')
from access_nba_data import epochtime

#strings for getting to file locations 
phone = ""
app_dir = "/home/martin/naismith/v1.1/"
sub_dir=app_dir+"nba_db_folder/"
filename='nba_data_test.sqlite'

#Grab date, season for consideration
season=raw_input('Season under consideration: ')
#season = 2016
cutdate=raw_input('Date to start from? e.g. JAN 1 2016: ')
#cutdate='Jan 1 2016'
cutdate=epochtime(cutdate)

model_start_date=raw_input('Date to start input to the model from? e.g. JAN 1 2016: ')
#model_start_date='dec 1 2015'
model_end_date=raw_input('Date to end input to the model from? e.g. JAN 1 2016: ')
#model_end_date='jan 1 2016'
model_start_date=epochtime(model_start_date)
model_end_date=epochtime(model_end_date)

#create ballrows list of tuples (all games) using the database
conn=sqlite3.connect(sub_dir+filename)
c=conn.cursor()
str_input='select id, datetime, start_time, away_team_id,away_pts,home_team_id,home_pts,date \
          from bballref_scores where season_year='+str(season)
ballrows=c.execute(str_input).fetchall()
#print('ballrows')
#pprint(ballrows)

#model data selection
c=conn.cursor()
str_input='select away_team_id,away_pts,home_team_id,home_pts \
          from bballref_scores where datetime >= '+str(model_start_date)+' AND datetime <'+str(model_end_date)
modelrows=c.execute(str_input).fetchall()

#Split data into games that have already occured and games that are to occur. Also grab a set of games
#for the model
futuredata=[row for row in ballrows if row[1]>=cutdate]
pastdata=[row for row in ballrows if row[1]<cutdate]
print(len(futuredata))
print(len(pastdata))

#Write out the results
list_to_csv(app_dir+'standings_projections/outfile_gms.csv',modelrows)
list_to_csv(app_dir+'standings_projections/outfile_future_games.csv',futuredata)
list_to_csv(app_dir+'standings_projections/outfile_past_games.csv',[row[3:7] for row in pastdata])








	
