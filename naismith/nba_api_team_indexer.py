from pprint import pprint

import sqlite3,os,csv
#from pprint import pprint

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

conn=sqlite3.connect(os.path.join(wkdir,'nba_data.sqlite'))
c=conn.cursor()

#Convert this to dict
#eliminate need for external csv by deleting the above code block
team_id_data_values=c.execute('select id, abbreviation, city, id, team_name,bball_ref_id,conf_or_league from pro_api_teams').fetchall()
team_id_data_keys=['id',' abbreviation', 'city',' id', 'team_name','bball_ref_id','conf_or_league']
team_id_data=[]
team_id_data_dict={}
for i in team_id_data_values:
  team_id_data_dict=dict(zip(team_id_data_keys,i))
  team_id_data.append(team_id_data_dict)

for id_set in team_id_data:
    #Away ids first
    game_ids=c.execute('SELECT id FROM nba_py_api_data WHERE away_TEAM_ID='+str(id_set['id'])).fetchall()
    game_ids=[g[0] for g in game_ids]
    for g in game_ids:
        up_str='UPDATE nba_py_api_data SET away_standard_id='+str(id_set['bball_ref_id'])+' WHERE id='+str(g)
        c.execute(up_str).fetchall()
    #Home ids after
    game_ids=c.execute('SELECT id FROM nba_py_api_data WHERE home_TEAM_ID='+str(id_set['id'])).fetchall()
    game_ids=[g[0] for g in game_ids]
    for g in game_ids:
        up_str='UPDATE nba_py_api_data SET home_standard_id='+str(id_set['bball_ref_id'])+' WHERE id='+str(g)
        c.execute(up_str).fetchall()

conn.commit()
conn.close()
