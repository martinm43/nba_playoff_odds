#MAM - 24 Sep 2016
#Adding models from another file.

#Parsing data obtained from basketball-reference.com 
#for use in analyses. Data to be used for Monte Carlo simulation.

#Replace Excel Program with Python routine. Get what you need.
import csv,os
from analytics.morey import SRS_regress,burke_regress

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

#This is the best way that I can think of to convert the team names into the 1-30 numbers required for 
#calculating SRS. Here goes...
def teamind ( str ):
	if str=='Atlanta Hawks':
		return 1
	if str=='Boston Celtics':
		return 2
	if str=='Brooklyn Nets':
		return 3
	if str=='Charlotte Hornets':
		return 4
	if str=='Chicago Bulls':
		return 5
	if str=='Cleveland Cavaliers':
		return 6
	if str=='Dallas Mavericks':
		return 7
	if str=='Denver Nuggets':
		return 8
	if str=='Detroit Pistons':
		return 9
	if str=='Golden State Warriors':
		return 10
	if str=='Houston Rockets':
		return 11
	if str=='Indiana Pacers':
		return 12
	if str=='Los Angeles Clippers':
		return 13
	if str=='Los Angeles Lakers':
		return 14
	if str=='Memphis Grizzlies':
		return 15
	if str=='Miami Heat':
		return 16
	if str=='Milwaukee Bucks':
		return 17
	if str=='Minnesota Timberwolves':
		return 18
	if str=='New Orleans Pelicans':
		return 19
	if str=='New York Knicks':
		return 20
	if str=='Oklahoma City Thunder':
		return 21
	if str=='Orlando Magic':
		return 22
	if str=='Philadelphia 76ers':
		return 23
	if str=='Phoenix Suns':
		return 24
	if str=='Portland Trail Blazers':
		return 25
	if str=='Sacramento Kings':
		return 26
	if str=='San Antonio Spurs':
		return 27
	if str=='Toronto Raptors':
		return 28
	if str=='Utah Jazz':
		return 29
	if str=='Washington Wizards':
		return 30
	else:
		return str
		
def team_name(index,tdicts):
  return [t['team_name'] for t in tdicts if t['team_id']==str(index)][0]

home_out=[]
away_out=[]
date_out=[]

#Use previously created list of future games
projdata=[]
with open(wkdir+'outfile_future_games.csv','rb') as futurefile:
	future_games_data = csv.reader(futurefile,delimiter=',')
	for row in future_games_data:
		projdata.append(row)
	futurefile.close

#pprint(projdata)

#Create the home and away vectors
for row in projdata:
#for row in future_data:
  date_out.append(row[7])
  home_out.append(row[5])
  away_out.append(row[3])

#print(future_data[0])
future_data=projdata

#Opening the calculated SRS or other measurement file
srs_data=[]
##obtaining ranks - choose ranking method based on user input
model_selection=raw_input('Please enter the type of model to be applied (if none, will be SRS*):')
if model_selection=='Burke':
	model_csv='burke_vector.csv'
	model_function=burke_regress
else:
	model_csv='SRS_vector.csv'
	model_function=SRS_regress

with open(wkdir+model_csv,'rb') as srsfile:
	rankdata = csv.reader(srsfile,delimiter=',')
	for row in rankdata:
		srs_data.append(row)
	srsfile.close

dsrs_data=[]
winpct_data=[]	
	
#Creating the dSRS and winpct vectors

for row in projdata:
	#what was the SRS difference?
	#convert row numbers into list indices by making them ints
	#and subtracting 1, grab SRS, then convert it into an int again
	#and grabs the first (and only) value in the single-entry list
	#checked as - print srs_data[int(row[2])-1][0]
	# print teamind(row[3])
	# print teamind(row[5])
	
	hsrs = float(srs_data[int(teamind(row[5]))-1][0])
	asrs = float(srs_data[int(teamind(row[3]))-1][0])

	dsrs = asrs-hsrs
    
	#No need to convert to string. Append does that for you.
	dsrs_data.append(dsrs)
	#print dsrs_str
	
	#what is the win percentage?
	winpct_data.append(model_function(dsrs))	




future_out=list(zip(home_out, away_out, dsrs_data, winpct_data)) 
	
#Part Two: Write out the "prediction" file.
csvfile_out = open(wkdir+'outfile_mcsims.csv','wb')
csvwriter = csv.writer(csvfile_out)
for row in future_out:
	#print(row)
	#Only need to print the visiting and home team scores and names.
	csvwriter.writerow(row)
csvfile_out.close()

#Print a "fancy/human readable" version of the above
fancy_out=list(zip(date_out,home_out, away_out, dsrs_data, winpct_data))
#print('fancyout')
#pprint(fancy_out[0])
fancy_out=[[row[0],team_name(row[1],teamdict),team_name(row[2],teamdict),row[3],row[4]] for row in fancy_out]
#pprint(fancy_out)
csvfile_out = open(wkdir+'coming_games_Excel.csv','wb')
csvwriter = csv.writer(csvfile_out)
csvwriter.writerow(['Date','Home Team','Away Team','dSRS','Home Team Win Probability'])
for row in fancy_out:
	#Only need to print the visiting and home team scores and names.
	csvwriter.writerow(row)
csvfile_out.close()

#List of known wins will be handled in the "season splitter" file from now on
#Martin Miller, Dec 20, 2016.



	
