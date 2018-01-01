#The purpose of this script/module
#is to use seemenow's nba_py module
#in order to generate information that can be used
#to update the nba_data.sqlite database

import nba_py, os, datetime
from dbtools.dbtools import table_initializer
from dbtools.access_nba_data import epochdate_nba_api,epochtime_nba_api
from dbtools.nba_data_models import NbaPyApiData
from teamind.teamind import teamind

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'
dbname='nba_data.sqlite'

#converting results to json by default even if pandas is available
#future iterations of this program may use pandas
nba_py.HAS_PANDAS=0

#Holder for month's game data.
month_games_list=[]

#Do this manually. 
now=datetime.datetime.now()

print('Gathering and consolidating NBA data from past days')
for i in range(7,0,-1): #starting from a week before.
    target_day=now-datetime.timedelta(days=i)
    g=nba_py.Scoreboard(day=target_day.day,month=target_day.month,year=target_day.year) 
    print('Processing data from '+target_day.__str__()[:10])
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
         g['GAME_DATE_EST']=gamedate
         g['full_date']=epochdate_nba_api(gamedate)
         g['day_datetime']=epochtime_nba_api(gamedate)
         g.pop('home_GAME_DATE_EST',None)
         g.pop('away_GAME_DATE_EST',None)
         month_games_list.append(g)
         #ids to be added later
         g['away_standard_id']=0
         g['home_standard_id']=0
         g['season_year']=2018 #hardcoded season
  
#Add a table containing the nba_py scoreboard data to the nba_data.sqlite database
#Using Peewee ORM

#1 - check result
gameslist=[dict((k.lower(), v) for k,v in g.iteritems()) for g in gameslist]
for g in gameslist:
  for k in g.keys():
    if k.endswith('_id'):
      k_new=k[:-3]
      g[k_new]=g[k]
      del g[k]

print('Consolidation complete, preparing to insert')
#2 - insert
NbaPyApiData.insert_many(gameslist).upsert().execute()
print('Data inserted into target database nba_data.sqlite')
