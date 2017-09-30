#-*-coding:utf8;-*-
#qpy:2
#qpy:console

import sqlite3,os,csv
from pprint import pprint
from dbtools.access_nba_data import epochtime
import numpy as np

#print "This is a SQL script executor"
db_folder=os.path.dirname(os.path.realpath(__file__))+'/'
sql_folder=os.path.dirname(os.path.realpath(__file__))+'/'
wkdir=os.path.dirname(os.path.realpath(__file__))+'/'

score_cut=raw_input('Please enter the maximum margin of victory/defeat (abs value): ')
score_cut=float(score_cut)

analysis_start_date=raw_input('Enter start date for analysis (e.g. Jan 1 2016): ')
analysis_end_date=raw_input('Enter end date for analysis (e.g. Feb 1 2016): ')
analysis_start_date=epochtime(analysis_start_date)
analysis_end_date=epochtime(analysis_end_date)
#analysis_start_date='Nov 1 2016'
#analysis_end_date='Dec 25 2016'

teamdict=[{'team_id':'1','team_name':'ATL','conf':'E'},
{'team_id':'2','team_name':'BOS','conf':'E'},
{'team_id':'3','team_name':'BRK','conf':'E'},
{'team_id':'4','team_name':'CHA','conf':'E'},
{'team_id':'5','team_name':'CHI','conf':'E'},
{'team_id':'6','team_name':'CLE','conf':'E'},
{'team_id':'7','team_name':'DAL','conf':'W'},
{'team_id':'8','team_name':'DEN','conf':'W'},
{'team_id':'9','team_name':'DET','conf':'E'},
{'team_id':'10','team_name':'GSW','conf':'W'},
{'team_id':'11','team_name':'HOU','conf':'W'},
{'team_id':'12','team_name':'IND','conf':'E'},
{'team_id':'13','team_name':'LAC','conf':'W'},
{'team_id':'14','team_name':'LAL','conf':'W'},
{'team_id':'15','team_name':'MEM','conf':'W'},
{'team_id':'16','team_name':'MIA','conf':'E'},
{'team_id':'17','team_name':'MIL','conf':'E'},
{'team_id':'18','team_name':'MIN','conf':'W'},
{'team_id':'19','team_name':'NOP','conf':'W'},
{'team_id':'20','team_name':'NYK','conf':'E'},
{'team_id':'21','team_name':'OKC','conf':'W'},
{'team_id':'22','team_name':'ORL','conf':'E'},
{'team_id':'23','team_name':'PHI','conf':'E'},
{'team_id':'24','team_name':'PHX','conf':'W'},
{'team_id':'25','team_name':'POR','conf':'W'},
{'team_id':'26','team_name':'SAC','conf':'W'},
{'team_id':'27','team_name':'SAS','conf':'W'},
{'team_id':'28','team_name':'TOR','conf':'E'},
{'team_id':'29','team_name':'UTA','conf':'W'},
{'team_id':'30','team_name':'WAS','conf':'E'}]

#Limit margin of victory
def score_bound(score_array,score_limit):
  import numpy as np
  score_array=score_array.clip(max=score_limit)
  score_array=score_array.clip(min=-score_limit)
  return score_array 
  
conn=sqlite3.connect(os.path.join(db_folder,'nba_data.sqlite'))
c=conn.cursor()

#print 'SQL script executor'
list_of_means=[]
vector_of_means=[]
for i in range(1,31):
  team_dict={}
  team_id=str(i)
  #Note the "2 pt" home advantage.
  #Incorporating Date Limits
  str_input='SELECT CASE WHEN away_standard_id='+team_id+\
           ' THEN away_pts-home_pts+2 WHEN home_standard_id='+team_id+\
           ' THEN home_pts-away_pts-2 END FROM nba_py_api_data WHERE\
           (away_standard_id='+team_id+' OR home_standard_id='+team_id+') AND '+\
           '(day_datetime >= '+str(analysis_start_date)+' AND day_datetime <= '+str(analysis_end_date)+');'

  if str_input.find('drop')==-1:
    query_result=c.execute(str_input).fetchall()
  #pprint(query_result)

  query_result=[q[0] for q in query_result]

  #filter out huge results
  scores=np.asarray(query_result)
  scores=score_bound(scores,score_cut)

  team_name=[row['team_name'] for row in teamdict if row['team_id']==team_id][0]
  print('Avg margin of victory for '+team_name+' : '+'{:1.4}'.format(scores.mean()))
  team_dict['team_name']=team_name
  team_dict['team_mean']=scores.mean()
  list_of_means.append(team_dict)
  vector_of_means.append([scores.mean()])
  team_dict={}
  
  
conn.close()

list_of_means.sort(key=lambda x:x['team_mean'], reverse=True)
pprint(list_of_means)

#Write list of trimmed point differentials to a file for use by other programs
csvfile_out = open(wkdir+'analytics/'+'adj_pts_diff_vector.csv','wb')
csvwriter = csv.writer(csvfile_out)
for row in vector_of_means:
    #Only need to print the visiting and home team scores and names.
    csvwriter.writerow(row)
csvfile_out.close()
