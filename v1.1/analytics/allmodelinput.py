#Martin Miller

#Model using data that will be available at all times.
#Because we have identified two important things:
#1. You should really just run this over the whole dataset
#2. You should really just give R a ton of data to model and play with


#Inputs
import numpy as np
import csv, os, sqlite3
import time
from pprint import pprint

#File data
phone = ""
app_dir = "/storage/emulated/0/download/"
sub_dir=app_dir+""
filename='nba_data_test.sqlite'

#point differential data function
def p_diff_data_query(team_id,game):
  #print 'select p_diff from bballref_avg_pts_diff where team_id='+str(team_id)+' and game_id='+str(game)
  return 'select p_diff from bballref_avg_pts_diff where team_id='+str(team_id)+' and game_id='+str(game)

#TOMORROW 17 SEP: Convert This To Return rest, and write another one for awaystreaks!!
def bballref_rest_query(team_id,game):
  #print 'select p_diff from bballref_avg_pts_diff where team_id='+str(team_id)+' and game_id='+str(game)
  return 'select resttime from bballref_rest where team_id='+str(team_id)+' and game_id='+str(game)
 
def bballref_away_query(team_id,game):
  #print 'select p_diff from bballref_avg_pts_diff where team_id='+str(team_id)+' and game_id='+str(game)
  return 'select away_streak from bballref_rest where team_id='+str(team_id)+' and game_id='+str(game)
 
#connect to database
conn=sqlite3.connect(sub_dir+filename)
c=conn.cursor()

#Choose a season
season=raw_input('Please enter a season to process: ')
league_season_game_results=[]

diff_model_input=[]
diff_model_input.append(['pdiff','is_away_b2b','is_home_b2b','win'])
  
for s in range(2007,2017):
  #Obtain all games from all teams for that season
  for i in range(1,31):
    team_games_id_query='select id from bballref_scores where (away_team_id ='+str(i)+' OR home_team_id ='+str(i)+') and season_year='+str(s)
    result=c.execute(team_games_id_query).fetchall()
    #if i==1:
      #pprint(result)
    league_season_game_results.append(result)
    # number of games in each season
    num_games=len(result)
    if len(result)>num_games:
      num_games=len(result)

  master_season_query='select id,home_team_id,away_team_id,home_pts-away_pts from bballref_scores where season_year='+str(s)
  season_games=c.execute(master_season_query).fetchall()
  #pprint(season_games)

  #print(len(season_games))

  #Create array of results. Each row corresponds to a unique team.
  league_season_games_array=np.array(league_season_game_results)

  #Create the array of outputs for each team
  #Start at first row.
  ind=1
  for g in season_games:
    print('Approx Percent Complete: '+"{:.3%}".format(ind*1.0/len(season_games))+' in season '+str(s))
    home_team_id=g[1]
    away_team_id=g[2]
    home_last_game=0
    away_last_game=0
    #pts data
    #get previous games played by participants
    home_prev_games_list=[game[0] for game in league_season_game_results[home_team_id-1] if game[0] < g[0]]
    away_prev_games_list=[game[0] for game in league_season_game_results[away_team_id-1] if game[0] < g[0]]
    if len(home_prev_games_list)>0:
       #last entry in list of games that occured before game in question
       home_last_game=home_prev_games_list[-1:][0]
    if len(away_prev_games_list)>0:
       away_last_game=away_prev_games_list[-1:][0]
	 
    if (home_last_game > 0) and (away_last_game > 0):
		  away_pts_diff=c.execute(p_diff_data_query(away_team_id,away_last_game)).fetchall()
		  home_pts_diff=c.execute(p_diff_data_query(home_team_id,home_last_game)).fetchall()
		
		  #If the query returns valid results
		  if home_pts_diff!=[] and away_pts_diff!=[]:
			   p_diff_input=home_pts_diff[0][0]-away_pts_diff[0][0]
			   #rest entering game (g[0])
			   away_rest=c.execute(bballref_rest_query(away_team_id,g[0])).fetchall()
			   away_rest=away_rest[0][0]
			   if away_rest < 24:
			     is_away_b2b=1
			   else:
			     is_away_b2b=0
			   home_rest=c.execute(bballref_rest_query(home_team_id,g[0])).fetchall()
			   home_rest=home_rest[0][0]
			   if home_rest < 24:
			     is_home_b2b=1
			   else:
			     is_home_b2b=0
			   #away team's travel streaks
			   away_streak=c.execute(bballref_away_query(away_team_id,g[0])).fetchall()
			   away_streak=away_streak[0][0]
			   #write these into an array
			   outcome=g[3]
			   diff_model_input.append([p_diff_input,away_rest,home_rest,outcome])
			   ind+=1
    else:
			   ind+=1
			   continue

#pprint(diff_model_input)
		
#Rest data
csvfile_out = open('/storage/emulated/0/download/line_model_input.csv','wb')
csvwriter = csv.writer(csvfile_out)
for row in diff_model_input:
	  csvwriter.writerow(row)
csvfile_out.close()		
	

#print(home_prev_games_list)
#print(away_prev_games_list)
#print([home_last_game,away_last_game])
  
#First game behind game in question - keep this for later (game before that id for team 0)
#print([game[0] for game in league_season_game_results[0] if game[0] < 20140099][0])

#Team rest data and away streaks 

#str_input='select id, datetime, start_time, away_team_id,away_pts,home_team_id,home_pts \
#          from bballref_rest where season_year='+str(season)

#Team +/- moving averages