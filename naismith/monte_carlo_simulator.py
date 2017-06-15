#Martin Miller, December 20, 2016
#This program prepares a  Monte Carlo Simulation over a period of the 2017 NBA season
#based on a static set of rankings for 30 teams

#Part I: Write out the future games and known wins.
#Part II: Write the simulation file and the set of games to be simulated

##########
# PART I #
##########

import csv, sqlite3, nba_py
import datetime
nba_py.HAS_PANDAS=False
import os
from access_nba_data import epochtime_numeric_month



#Working directory.
wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

#CSV output function
def list_to_csv(csvfile,list_of_lists):
    import csv
    csvfile_out = open(csvfile,'wb')
    csvwriter = csv.writer(csvfile_out)
    for row in list_of_lists:
        #Only need to print the visiting and home team scores and names.
        csvwriter.writerow(row)
    csvfile_out.close()
    return 1

#Read NBA team ids into a data structure from a known file of team names.
team_id_data=[]
target='pro_api_teams.csv'
with open(wkdir+target,'rb') as csvfile:
    balldata = csv.reader(csvfile,delimiter=',')
    team_id_dict={}
    for row in balldata:
        team_id_dict['nba_api_id']=int(row[0])
        team_id_dict['standard_id']=int(row[5])
        team_id_data.append(team_id_dict)
        team_id_dict={} #clear holder
    csvfile.close
    
#strings for getting to file locations 
wkdir = os.path.dirname(os.path.realpath(__file__))+'/'
filename='nba_data_test.sqlite'

#Hardcoded for ease of testing/practical concerns
season=2017
#year=2016
#standings_scoreboard_month=12
#standings_scoreboard_day=18
now=datetime.datetime.now()
year=now.year
standings_scoreboard_month=now.month
standings_scoreboard_day=now.day

cutdate_str=str(standings_scoreboard_month)+' '+str(standings_scoreboard_day)+' '+str(year)
cutdate=epochtime_numeric_month(cutdate_str)

#Obtain eastern and western standings and then use them (to create a list of known wins)
standings_scoreboard=nba_py.Scoreboard(month=standings_scoreboard_month, day=standings_scoreboard_day)
east_standings=standings_scoreboard.east_conf_standings_by_day()
west_standings=standings_scoreboard.west_conf_standings_by_day()
standings=east_standings+west_standings
for standings_team in standings:
    team_standard_id=[team['standard_id'] for team in team_id_data if team['nba_api_id']==standings_team['TEAM_ID']][0]
    standings_team['standard_id']=team_standard_id

#create ballrows list of tuples (all games) using the database
conn=sqlite3.connect(wkdir+filename)
c=conn.cursor()
str_input='select id, datetime, start_time, away_team_id,away_pts,home_team_id,home_pts,date \
          from bballref_scores where season_year='+str(season)
ballrows=c.execute(str_input).fetchall()
#print('ballrows')
#pprint(ballrows)

#Split data into games that have already occured and games that are to occur. Also grab a set of games
#for the model
futuredata=[row for row in ballrows if row[1]>=cutdate]
pastdata=[row for row in ballrows if row[1]<cutdate]
print('Number of games to be played: '+str(len(futuredata)))
print('Number of games already played: '+str(len(pastdata)))

#Write out the results
list_to_csv(wkdir+'outfile_future_games.csv',futuredata)

#TO DO
#Change above logic for splitting season to generate a day and month
#Obtain win/loss records using Scoreboard.E/W Standings By Day and write out W/L to 
#ouftile_wins.csv

#Merge this with the Monte_Carlo_Calculations and Monte_Carlo_Simulation script
#Handle differing simulation methods by using vectorized version as estimate
#No reason that a 300 line or so script can't be used to do this








	
