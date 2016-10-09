def team_rest_calc(ballrows):

  import csv, os, time, datetime
  import numpy as np

  #Calculate rest between games, and (later) travel between games, for each 
  #team.
  #For each team create a numpy array containing
  #1. team id
  #2. game id
  #3. datetime (seconds since epoch)
  #4. rest time in hours since last game
  #5. unique id
  #6. 
  srd_headers=['team_id','game_id','datetime','resttime','id']
  season_rest_data=[]
  for i in range(1,31):
    print('Calculating rest days for games of team '+str(i))
    #NB: need to softcode this because of strike seasons
    team_game_ids=[(i,row["id"],row["datetime"]) for row in ballrows\
                if (row["away_team_id"]==i or row["home_team_id"]==i)]
    team_time_data=np.zeros((len(team_game_ids),4))
    team_game_ids=np.asarray(team_game_ids)
    if len(team_game_ids)>0:
      team_time_data[:,:-1]=team_game_ids
    else:
      print 'Warning: Team '+str(i)+' not found'
    for j in range(1,len(team_game_ids)): #skip the first game with index 0. 82 games in season.
       #Calculate time in hours between games
       team_time_data[j,3]=(team_game_ids[j,2]-team_game_ids[j-1,2])/3600.0 
       #Is it an away game?
       #if [row['away_team_id'] for row in ballrows if row['id']==team_game_ids[j,1]][0]==i:
         #print 'Away'
       #else:
         #print 'Home'  
    team_time_data=team_time_data.tolist()
    
    #zip each list with the dictionary key
    for game in team_time_data:
      game=dict(zip(srd_headers,game))
      season_rest_data.append(game)
      #print game


  return season_rest_data

######################
# UNDER DEVELOPMENT. #
######################

def team_rest_calc_v2(ballrows):

  #Calculate rest between games, and (later) travel between games, for each 
  #team.
  #For each team create a numpy array containing
  #1. team id
  #2. game id
  #3. datetime (seconds since epoch)
  #4. rest time in hours since last game
  #5. unique id
  #6. is away?
  
  import csv, os, time, datetime
  import numpy as np
  
  srd_headers=['team_id','game_id','datetime','resttime','id','is_away','away_streak']
  season_rest_data=[]
  for i in range(1,31):
    print('Calculating rest days for games of team '+str(i))
    #NB: need to softcode this because of strike seasons
    team_game_ids=[(i,row["id"],row["datetime"]) for row in ballrows\
                if (row["away_team_id"]==i or row["home_team_id"]==i)]
    team_time_data=np.zeros((len(team_game_ids),7))
    team_game_ids=np.asarray(team_game_ids)
    if len(team_game_ids)>0:
      team_time_data[:,:-4]=team_game_ids
    else:
      print 'Warning: Team '+str(i)+' not found'
    for j in range(1,len(team_game_ids)): #skip the first game with index 0. 82 games in season.
       #Calculate time in hours between games
       team_time_data[j,3]=(team_game_ids[j,2]-team_game_ids[j-1,2])/3600.0 
       #Is it an away game?
       #Be sure to count them.
       count_away=0
       if [row['away_team_id'] for row in ballrows if row['id']==team_game_ids[j,1]][0]==i:
         team_time_data[j,5]=1
         count_away=1
         for k in range(j,0,-1):
           if team_time_data[k,5]==1:
             count_away+=1
           else:
             break
         team_time_data[j,6]=count_away
          
    team_time_data=team_time_data.tolist()
    
    #zip each list with the dictionary key
    for game in team_time_data:
      #print game
      #print srd_headers
      game=dict(zip(srd_headers,game))
      season_rest_data.append(game)
      


  return season_rest_data
