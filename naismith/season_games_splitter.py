"""
Season Games Splitter

This program splits the season into "games that have already been played"
and determines which games have already been won.

Automatic mode is triggered by adding "AUTO" to the script invocation.
In automatic mode, the current season is cut based on the current date 
(Not yet implemented.)

--MA Miller

"""


#Replace Excel Program with Python routine.
import sqlite3
import os,sys,time
#get the conversion function
from dbtools.access_nba_data import epochtime

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

season=raw_input('Season under consideration: ')
cutdate=raw_input('Date to start from? e.g. JAN 1 2016: ')

#strings for getting to file locations 
wkdir = os.path.dirname(os.path.realpath(__file__))+'/'
filename='nba_data.sqlite'

season_start=epochtime('Oct 15 '+season)-31536000
cutdate=epochtime(cutdate)

#create ballrows list of tuples (all games) using the database
conn=sqlite3.connect(wkdir+filename)
c=conn.cursor()
str_input='select id, datetime, start_time, away_team_id,away_pts,home_team_id,home_pts,date \
          from bballref_scores where season_year='+str(season)
ballrows=c.execute(str_input).fetchall()

#Dec 29 2016 edit: Obtain an up-to-date list of wins from the nba_py_api_data database
c=conn.cursor()
str_input='SELECT away_standard_id, away_pts, home_standard_id, home_pts FROM nba_py_api_data WHERE day_datetime<='+str(cutdate)+' AND day_datetime >= '+str(season_start)
gameslist=c.execute(str_input).fetchall()
#Hardcoded solution to "incorporating past wins while projecting into the future" problem
winlist=[x[0] if x[1]>x[3] else x[2] for x in gameslist]
#winlist=[0 for x in gameslist]

winrows=[]
for i in range(1,31):
    winrows.append([winlist.count(i)])

#Split data into games that have already occured and games that are to occur. Also grab a set of games
#for the model
futuredata=[row for row in ballrows if row[1]>=cutdate]
pastdata=[row for row in ballrows if row[1]<cutdate]
print('Number of games to be played: '+str(len(futuredata)))
print('Number of games already played: '+str(len(pastdata)))

#Write out the results
list_to_csv(wkdir+'outfile_wins.csv',winrows)
list_to_csv(wkdir+'outfile_future_games.csv',futuredata)

