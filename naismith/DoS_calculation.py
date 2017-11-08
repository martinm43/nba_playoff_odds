# coding: utf-8
from __future__ import division
#from pprint import pprint
import numpy as np
from dbtools.nba_data_models import database, NbaPyApiData, BballrefScores, NbaTeamEloData
from dbtools.access_nba_data import epochtime #, stringtime
from DoS_optimization import dos,expected_dos
from string_conversion_tools import team_abbreviation

from dbtools.max_sql_variables import max_sql_variables
SQLITE_MAX_VARIABLE_NUMBER=max_sql_variables()

#defaults
init_rank=1500.0
 #what a "neutral team" is valued at
dos_factor=27 #factor applied to change value based on expected performance vs actual
def_env_factor=75 #environment factor for away team
def_expect_factor=1.0 #affects sigmoid plot of -1 to +1 outcomes based on quality diff.


#Choosing to use year-based calculations to deal with trading problems
#Zero teach team out at beginning of year, reperform calculations each year
start_season_year=2017
end_season_year=2017

#Looping begins here
list_of_team_score_dicts=[]

for i in range(start_season_year,end_season_year+1): 
  #following other table conventions
  season_year=i
  start_date=epochtime('Oct 1 '+str(season_year))
  end_date=epochtime('May 1 '+str(season_year+1))

  #arrays
  ranks=np.ones(30)*init_rank

  s=NbaPyApiData.select().where(NbaPyApiData.day_datetime>=start_date,\
                                NbaPyApiData.day_datetime<=end_date)

  s_b=BballrefScores.select().where(BballrefScores.datetime>=start_date,\
                                BballrefScores.datetime<=end_date)


  #nba py api version
  #s_array=[(i.away_standard,i.away_pts,i.home_standard,i.home_pts) for i in s]
  #bballref version
  s_array=[(i.away_team_id,i.away_pts,i.home_team_id,i.home_pts,i.datetime) for i in s_b]
  s_date_array=[(i.datetime) for i in s_b]

  error=0
  data_indexer=1

  for i in s_array:
      if i[1]>0 and i[3]>0:
          away_rank=ranks[i[0]-1]
          home_rank=ranks[i[2]-1]
          expected_away_diff=expected_dos(away_rank,home_rank,env_factor=def_env_factor,expect_factor=def_expect_factor)
          expected_home_diff=expected_dos(home_rank,away_rank,env_factor=def_env_factor,expect_factor=def_expect_factor)
          away_diff=dos_factor*(dos(i[1],i[3])-expected_away_diff)
          home_diff=dos_factor*(dos(i[3],i[1])-expected_home_diff)
          error+=(dos(i[1],i[3])-expected_away_diff)**2+(dos(i[3],i[1])-expected_home_diff)**2
          ranks[i[0]-1]=away_rank+away_diff
          ranks[i[2]-1]=home_rank+home_diff
          for j in enumerate(ranks):
              list_of_team_score_dicts.append({'id':season_year*100000+data_indexer,\
                                               
                                               #Note that to follow bballref
                                               #this year has to be one year
                                               #after season start year
                                               'season_year':season_year+1,\
                                               
                                               
                                               'datetime':i[4],\
                                               'team_abbreviation':team_abbreviation(j[0]+1),\
                                               'elo_rating':j[1]})
              data_indexer+=1


with database.atomic() as txn:
     size = (SQLITE_MAX_VARIABLE_NUMBER // len(list_of_team_score_dicts[0])) - 1 
     # remove one to avoid issue if peewee adds some variable
     for i in range(0, len(list_of_team_score_dicts), size):NbaTeamEloData.insert_many(list_of_team_score_dicts[i:i+size]).upsert().execute()
  
