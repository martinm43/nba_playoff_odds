import os
import csv
import numpy as np

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
print('testing naming function, id=1')
print(id_to_name(1,teamdict))

#get teams and games win probability from previous csv
mcrows = []
with open(wkdir+'outfile_mcsims.csv','rb') as csvfile:
	balldata = csv.reader(csvfile,delimiter=',')
	for row in balldata:
		mcrows.append(row)
	csvfile.close

#get known wins!
winrows = []
with open(wkdir+'outfile_wins.csv','rb') as csvfile:
	balldata = csv.reader(csvfile,delimiter=',')
	for row in balldata:
         win=int(row[0])
         winrows.append(win)
	csvfile.close	
 
 
mcrows=np.asarray(mcrows,dtype=float)
hometeams=mcrows[:,0].T
awayteams=mcrows[:,1].T
gamepairs=mcrows[:,0:1]
#pprint(gamepairs[0])
winprobs=mcrows[:,3].T

#print(hometeams)

ngames=len(winprobs)
nsims=10000

print('Performing vectorized Python Monte Carlo Simulation.')
print('Number of simulations set at '+str(nsims)+' simulations')
print('Value can be changed within script, however, memory considerations limit it e.g. to approx')
print('~100000 simulations at a time on an 8GB memory computer')


mcsimgames=np.random.uniform(size=(ngames,nsims))

#print(mcsimgames.shape)

simwinprobs=np.tile(winprobs,(nsims,1)).T


#print(simwinprobs.T.shape)
#print(simwinprobs)
awaywins=mcsimgames<simwinprobs
homewins=np.invert(awaywins)

awaywins=np.asarray(awaywins,dtype=int)
homewins=np.asarray(homewins,dtype=int)

#print(awaywins)
#print(homewins)

awayteams=np.tile(awayteams,(nsims,1)).T
hometeams=np.tile(hometeams,(nsims,1)).T
print(hometeams.shape)
win_away_teams_array=np.multiply(awayteams,awaywins)
win_home_teams_array=np.multiply(hometeams,homewins)

avg_wins_list=[]

for i in range(1,31):
  team_id=i
  away_team_win_array=win_away_teams_array==team_id
  home_team_win_array=win_home_teams_array==team_id
  away_team_win_array=np.asarray(away_team_win_array,dtype=int)
  home_team_win_array=np.asarray(home_team_win_array,dtype=int)
  avg_wins_list.append(np.sum(away_team_win_array)/nsims+np.sum(home_team_win_array)/nsims)


avwins=[x+y for x,y in zip(avg_wins_list,winrows)] #list comprehension + zip
ite=nsims

#Print to screen
i=1
biglist=[]
print 'Team (Conf): Median Wins'
for t in avwins:
   slist=[]
   slist.append([row['team_name'] for row in teamdict if row['team_id']==str(i)][0])
   slist.append([row['conf'] for row in teamdict if row['team_id']==str(i)][0])
   slist.append(t) 
   biglist.append(slist)
   i = i + 1

#use lambda exp to sort by column
biglist.sort(key=lambda x:x[2],reverse=True)

west = [row for row in biglist if row[1]=='W']
east = [row for row in biglist if row[1]=='E']

#printing scheme for seeds
print 'West'
i=1
for t in west:
#   print str(i)+': \t'+t[0] +' \t'+str(t[2])
   i=i+1
print '\n'
print 'East'
i=1
for t in east:
#   print str(i)+': \t'+t[0] +' \t'+str(t[2])
   i=i+1

print 'Number of Simulations: ' + str(ite)

csvfile_out = open(wkdir+'MC_sim_results_Excel.txt','wb')
csvwriter = csv.writer(csvfile_out)

#Write a header row for the csv
csvwriter.writerow(['Rank','Team','Conference','Wins'])

i=1
for t in enumerate(west):
   print t
   csvwriter.writerow([str(t[0]+1),t[1][0],t[1][1],t[1][2]])

i=1
for t in enumerate(east):
   print t
   csvwriter.writerow([str(t[0]+1),t[1][0],t[1][1],t[1][2]])


#Reporting playoff odds
# for i in range(1,31):
	# oddsrow='Team '+id_to_name(i,teamdict)+' has a playoff probability of '+'{0:.4%}'.format(float(playoff_results.count(i))/float(ite))
	# print(oddsrow)
	# csvwriter.writerow([oddsrow])

csvwriter.writerow(['Number of Simulations: '+str(ite)])
csvfile_out.close()

print('Simulation Complete!')
