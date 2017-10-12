#The purpose of this script/module
#is to use seemenow's nba_py module
#in order to generate information that can be used
#to update the nba_data.sqlite database

import nba_py, os, datetime
from dbtools.dbtools import table_initializer
from dbtools.access_nba_data import epochdate_nba_api,epochtime_nba_api
from dbtools.nba_data_models import NbaPyApiData
from pprint import pprint

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'
dbname='nba_data.sqlite'

#converting results to json by default even if pandas is available
#future iterations of this program may use pandas
nba_py.HAS_PANDAS=0

#Holder for month's game data.
month_games_list=[]

#Do this manually. 
#scoreboard_month=raw_input('Enter month to update(1-12 format): ')
#scoreboard_month=int(scoreboard_month)
now=datetime.datetime.now()
scoreboard_month=now.month
scoreboard_min_day=max(now.day-3,1) #careful to keep a min day.
scoreboard_max_day=now.day-1

#single day edit
##scoreboard_month=12
##scoreboard_min_day=28
##scoreboard_max_day=31

for scoreboard_day in range(scoreboard_min_day, scoreboard_max_day+1):
    g=nba_py.Scoreboard(day=scoreboard_day,month=scoreboard_month) #if updating pre 2017 add year.
    #Obtain game information from the "linescore" method of the Scoreboard class
    #This data is arranged in pairs. Odd teams are away teams and even teams are home teams.
    line_score_list=g.line_score()
     #Create a new list of dicts, where each dict constitutes a game.
    #Use odd and even away and home game logic to add "away" and "home" to defined values.
    gameslist=[]
    game={}
    is_away_team=True
    num_teams=0 #track the number of teams in each game pair and cut each pair when done
    for line in line_score_list:
        if is_away_team==True:
            for l in line.keys():
                game['away_'+l]=line[l]
        elif is_away_team==False:
            for l in line.keys():
                game['home_'+l]=line[l]
        is_away_team = not is_away_team #next team by default is the opposite home sit'n of the current team
        #print is_away_team
        num_teams+=1
        if num_teams==2:
            gameslist.append(game)
            game={} #Must clear the temporary game container prior to proceeding to the next pair
            num_teams=0

    #Consolidating and removing redundant keys in each game in the day
    for g in gameslist:
         g['id']=g['home_GAME_ID']
         g.pop('home_GAME_ID',None)
         g.pop('away_GAME_ID',None)
         #game date - condensed
         gamedate=g['home_GAME_DATE_EST']
         gamedate=gamedate[:10]
         print(gamedate)
         g['GAME_DATE_EST']=gamedate
         g['full_date']=epochdate_nba_api(gamedate)
         g['day_datetime']=epochtime_nba_api(gamedate)
         print(g['full_date'])
         g.pop('home_GAME_DATE_EST',None)
         g.pop('away_GAME_DATE_EST',None)
         month_games_list.append(g)
         #ids to be added later
         g['away_standard_id']=0
         g['home_standard_id']=0
  
#Add a table containing the nba_py scoreboard data to the nba_data.sqlite database
#print('Preparing to write to nba working database. Please stand by...')

#tablename='nba_py_api_data'

#table_initializer(wkdir+dbname,tablename,month_games_list[0],month_games_list,automode='on')

#Using Peewee ORM

#1 - check result
gameslist=[dict((k.lower(), v) for k,v in g.iteritems()) for g in gameslist]
for g in gameslist:
  for k in g.keys():
    if k.endswith('_id'):
      k_new=k[:-3]
      g[k_new]=g[k]
      del g[k]

pprint(gameslist)
#2 - insert
NbaPyApiData.insert_many(gameslist).upsert().execute()
