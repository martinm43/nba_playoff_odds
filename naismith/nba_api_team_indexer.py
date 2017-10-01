#-*-coding:utf8;-*-
#qpy:2
#qpy:console

from pprint import pprint

import sqlite3,os,csv
#from pprint import pprint

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

conn=sqlite3.connect(os.path.join(wkdir,'nba_data.sqlite'))
c=conn.cursor()

#team_id_data=[]
#target='pro_api_teams_list.csv'
#with open(wkdir+target,'rb') as csvfile:
#    balldata = csv.reader(csvfile,delimiter=',')
#    team_id_dict={}
#    for row in balldata:
#        team_id_dict['nba_api_id']=int(row[0])
#        team_id_dict['standard_id']=int(row[5])
#        team_id_data.append(team_id_dict)
#        team_id_dict={} #clear holder
#    csvfile.close

#Convert this to dict
#eliminate need for external csv by deleting the above code block
team_id_data_values=c.execute('select id, abbreviation, city, id, team_name,bball_ref_id,conf_or_league from pro_api_teams').fetchall()
#print(team_id_data_values[0])
team_id_data_keys=['id',' abbreviation', 'city',' id', 'team_name','bball_ref_id','conf_or_league']
team_id_data=[]
team_id_data_dict={}
for i in team_id_data_values:
  team_id_data_dict=dict(zip(team_id_data_keys,i))
  #print(team_id_data_dict)
  team_id_data.append(team_id_data_dict)
#pprint(team_id_data)

for id_set in team_id_data:
    #Away ids first
    #pprint(id_set.keys())
    game_ids=c.execute('SELECT id FROM nba_py_api_data WHERE away_TEAM_ID='+str(id_set['id'])).fetchall()
    game_ids=[g[0] for g in game_ids]
    for g in game_ids:
        up_str='UPDATE nba_py_api_data SET away_standard_id='+str(id_set['bball_ref_id'])+' WHERE id='+str(g)
        #print(up_str)
        c.execute(up_str).fetchall()
    #Home ids after
    game_ids=c.execute('SELECT id FROM nba_py_api_data WHERE home_TEAM_ID='+str(id_set['id'])).fetchall()
    game_ids=[g[0] for g in game_ids]
    for g in game_ids:
        up_str='UPDATE nba_py_api_data SET home_standard_id='+str(id_set['bball_ref_id'])+' WHERE id='+str(g)
        #print(up_str)
        c.execute(up_str).fetchall()


  
conn.commit()
conn.close()
