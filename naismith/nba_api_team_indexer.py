#-*-coding:utf8;-*-
#qpy:2
#qpy:console

print "This scripts links the stats.nba.com api ids with regular ids"

import sqlite3,os,csv
#from pprint import pprint

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

conn=sqlite3.connect(os.path.join(wkdir,'nba_data.sqlite'))
c=conn.cursor()

team_id_data=[]
target='pro_api_teams_list.csv'
with open(wkdir+target,'rb') as csvfile:
    balldata = csv.reader(csvfile,delimiter=',')
    team_id_dict={}
    for row in balldata:
        team_id_dict['nba_api_id']=int(row[0])
        team_id_dict['standard_id']=int(row[5])
        team_id_data.append(team_id_dict)
        team_id_dict={} #clear holder
    csvfile.close

#Convert this to dict
#eliminate need for external csv by deleting the above code block
team_id_data==c.execute('select id, abbreviation, city, id, team_name,bball_ref_id,conf_or_league from pro_api_teams')

for id_set in team_id_data:
    #Away ids first
    game_ids=c.execute('SELECT id FROM nba_py_api_data WHERE away_TEAM_ID='+str(id_set['nba_api_id'])).fetchall()
    game_ids=[g[0] for g in game_ids]
    for g in game_ids:
        up_str='UPDATE nba_py_api_data SET away_standard_id='+str(id_set['standard_id'])+' WHERE id='+str(g)
        print(up_str)
        c.execute(up_str).fetchall()
    #Home ids after
    game_ids=c.execute('SELECT id FROM nba_py_api_data WHERE home_TEAM_ID='+str(id_set['nba_api_id'])).fetchall()
    game_ids=[g[0] for g in game_ids]
    for g in game_ids:
        up_str='UPDATE nba_py_api_data SET home_standard_id='+str(id_set['standard_id'])+' WHERE id='+str(g)
        print(up_str)
        c.execute(up_str).fetchall()


  
conn.commit()
conn.close()
