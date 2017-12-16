#MAM - 24 Sep 2016
#Adding models from another file.

#Parsing data obtained from basketball-reference.com 
#for use in analyses. Data to be used for Monte Carlo simulation.

#Replace Excel Program with Python routine. Get what you need.
import csv,os
from analytics.morey import SRS_regress,burke_regress,pts_regress
from teamind.teamind import teamind
from string_conversion_tools import team_abbreviation

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

#teamdict=[{'team_id':'1','team_name':'ATL','conf':'E'},
#{'team_id':'2','team_name':'BOS','conf':'E'},
#{'team_id':'3','team_name':'BRK','conf':'E'},
#{'team_id':'4','team_name':'CHA','conf':'E'},
#{'team_id':'5','team_name':'CHI','conf':'E'},
#{'team_id':'6','team_name':'CLE','conf':'E'},
#{'team_id':'7','team_name':'DAL','conf':'W'},
#{'team_id':'8','team_name':'DEN','conf':'W'},
#{'team_id':'9','team_name':'DET','conf':'E'},
#{'team_id':'10','team_name':'GSW','conf':'W'},
#{'team_id':'11','team_name':'HOU','conf':'W'},
#{'team_id':'12','team_name':'IND','conf':'E'},
#{'team_id':'13','team_name':'LAC','conf':'W'},
#{'team_id':'14','team_name':'LAL','conf':'W'},
#{'team_id':'15','team_name':'MEM','conf':'W'},
#{'team_id':'16','team_name':'MIA','conf':'E'},
#{'team_id':'17','team_name':'MIL','conf':'E'},
#{'team_id':'18','team_name':'MIN','conf':'W'},
#{'team_id':'19','team_name':'NOP','conf':'W'},
#{'team_id':'20','team_name':'NYK','conf':'E'},
#{'team_id':'21','team_name':'OKC','conf':'W'},
#{'team_id':'22','team_name':'ORL','conf':'E'},
#{'team_id':'23','team_name':'PHI','conf':'E'},
#{'team_id':'24','team_name':'PHX','conf':'W'},
#{'team_id':'25','team_name':'POR','conf':'W'},
#{'team_id':'26','team_name':'SAC','conf':'W'},
#{'team_id':'27','team_name':'SAS','conf':'W'},
#{'team_id':'28','team_name':'TOR','conf':'E'},
#{'team_id':'29','team_name':'UTA','conf':'W'},
#{'team_id':'30','team_name':'WAS','conf':'E'}]

#def team_name(index,tdicts):
#  return [t['team_name'] for t in tdicts if t['team_id']==str(index)][0]

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
print('Model selection: ')
print('Model 1: Points')
print('Model 2: Burke (accounts for SoS and home strength)')
model_selection=input('Please enter the type of model to be applied: ')
if model_selection==1:
	model_csv='burke_vector.csv'
	model_function=burke_regress
if model_selection==2:
	model_csv='analytics/adj_pts_diff_vector.csv'
	model_function=pts_regress

#SRS functionality broken:
#else:
#	model_csv='SRS_vector.csv'
#	model_function=SRS_regress

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
fancy_out=[[row[0],team_abbreviation(row[1]),team_abbreviation(row[2]),row[3],row[4]] for row in fancy_out]
#pprint(fancy_out)
csvfile_out = open(wkdir+'coming_games_Excel.csv','wb')
csvwriter = csv.writer(csvfile_out)
csvwriter.writerow(['Date','Home Team','Away Team','Differential','Away Team Win Probability'])
for row in fancy_out:
	#Only need to print the visiting and home team scores and names.
	csvwriter.writerow(row)
csvfile_out.close()

#List of known wins will be handled in the "season splitter" file from now on
#Martin Miller, Dec 20, 2016.



	
