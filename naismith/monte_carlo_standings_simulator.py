"""
Monte Carlo Standings Simulator

Determines average projected positions and odds of each team making the playoffs.

"""
from __future__ import division

import csv
import os
import random
import numpy as np
import datetime
from tabulate import tabulate

#
now=datetime.datetime.now()

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

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

def id_to_name(team_id,league_dicts):
  return [d['team_name'] for d in league_dicts if d['team_id']==str(team_id)][0]



mcrows = []
with open(wkdir+'outfile_mcsims.csv','rb') as csvfile:
    balldata = csv.reader(csvfile,delimiter=',')
    for row in balldata:
        mcrows.append(row)

#get known wins
winrows = []
with open(wkdir+'outfile_wins.csv','rb') as csvfile:
    balldata = csv.reader(csvfile,delimiter=',')
    for row in balldata:
        winrows.append(row)



#Flatten to be of use, while converting into int, then convert into array:
winrows = [int(val) for sublist in winrows for val in sublist]
winrows = np.asarray(winrows)

all_sims = []

#Automatic mode has hardcoded number of simulations.
ite=1

print('Number of pending iterations: '+str(ite))

for i in range (ite):
    sim_dat=[]
    sim_dat_gen=[row[1] if random.uniform(0,1) < float(row[3]) else row[0] for row in mcrows]
    #Calculate number of wins for each team
    simwinlist=[sim_dat_gen.count(str(i)) for i in range(1,31)]
    #convert and add known wins then convert back into a list
    simwinlist = np.asarray(simwinlist)
    simwinlist = np.add(winrows,simwinlist)
    simwinlist=simwinlist.tolist()
    
    #append to grand list
    all_sims.append(simwinlist)

#October 10, 2016 - MAM
#Calculating estimated playoff odds based on number of playoff appearances (rank > 8 in conference)
#It is assumed that any tiebreakers are rendered irrelevant by a large number of simulations
#Create an array for holding all data
playoff_results=[]
for row in all_sims:
    #Create a modified version of the team dicts containing the number of wins for each row
    pdict=teamdict
    for p in pdict:
        p['wins']=row[int(p['team_id'])-1]
    eastteams=[p for p in pdict if p['conf']=='E']
    westteams=[p for p in pdict if p['conf']=='W']
    #Sort by the 'wins' column
    eastteams.sort(key=lambda x:x['wins'],reverse=True)
    westteams.sort(key=lambda x:x['wins'],reverse=True)
    #Add the winning teams to the playoff_results array
    for i in range(0,8):
        playoff_results.append(int(eastteams[i]['team_id']))
        playoff_results.append(int(westteams[i]['team_id']))

avwins=np.percentile(all_sims,50,axis=0)

###Print to screen and to file###

i=1
biglist=[]

for t in avwins:
   slist=[]
   slist.append([row['team_name'] for row in teamdict if row['team_id']==str(i)][0])
   slist.append([row['conf'] for row in teamdict if row['team_id']==str(i)][0])
   slist.append(t) 
   biglist.append(slist)
   i = i + 1

#use lambda exp to sort by column
biglist.sort(key=lambda x:x[2],reverse=True)

#Extract average wins and team abbreviations.
west = [row for row in biglist if row[1]=='W']
east = [row for row in biglist if row[1]=='E']
west = [i[1] for i in enumerate(west)]
east = [i[1] for i in enumerate(east)]
west = [[i[0],i[2]] for i in west]
east = [[i[0],i[2]] for i in east]

west_table=tabulate(west,headers=["Team Name","Average Wins in Simulations"])
east_table=tabulate(east,headers=["Team Name","Average Wins in Simulations"])

print 'Summary of Results, '+now.strftime('%Y-%m-%d')+'\n'

print 'Total number of iterations: '+str(ite)+'\n'

print 'Western Conference\n'
print west_table
print '\n'
print 'Eastern Conference\n'
print east_table
print '\n\n'
print 'Playoff Odds For Each Team\n'

#Reporting playoff odds
for i in range(1,31):
    oddsrow=id_to_name(i,teamdict)+' has '+'{:.4g}%'.format(float(playoff_results.count(i))/float(ite)*100.00)+' chance of making the playoffs\n'
    print(oddsrow)

print 'Writing to file.'

#Repeat commands above but write the information to a file.

file_out = open(wkdir+'Summary_'+str(ite)+'_iter_'+now.strftime('%Y-%m-%d')+'.txt','wb')

file_out.write('Summary of Results, '+now.strftime('%Y-%m-%d')+'\n\n')

file_out.write('Total number of iterations: '+str(ite)+'\n\n')

file_out.write('Western Conference\n')
file_out.write(west_table)
file_out.write('\n\n')
file_out.write('Eastern Conference\n')
file_out.write(east_table)
file_out.write('\n\n')

file_out.write('Estimated Odds of Making the Playoffs For Each Team\n')

#Reporting playoff odds
for i in range(1,31):
    oddsrow=id_to_name(i,teamdict)+' has '+'{:.4g}%'.format(float(playoff_results.count(i))/float(ite)*100.00)+' chance of making the playoffs\n'
    file_out.write('Playoff Odds For Each Team\n')

file_out.close()

