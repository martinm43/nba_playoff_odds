"""

Monte Carlo Calculations

Uses one of a set of static team ratings previously generated in order to generate 
* a csv for use in monte carlo simulation
* an Excel file for seeing upcoming games

Human automation requirements: choosing a preferred solution method
Ascending numbers should denote "fancier" solution methods. 

As of Dec 25 2017, method is 2 - Burke (Accounts for SOS and HTA)

"""


import csv,os,xlsxwriter
from analytics.morey import SRS_regress,burke_regress,pts_regress
from teamind.teamind import teamind
from string_conversion_tools import team_abbreviation
import datetime

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

home_out=[]
away_out=[]
date_out=[]

#datestring.
now=datetime.datetime.now()
now_str=now.strftime('%Y-%m-%d')

#Use previously created list of future games
projdata=[]
with open(wkdir+'outfile_future_games.csv','rb') as futurefile:
	future_games_data = csv.reader(futurefile,delimiter=',')
	for row in future_games_data:
		projdata.append(row)
	futurefile.close


#Create the home and away vectors
for row in projdata:
  date_out.append(row[7])
  home_out.append(row[5])
  away_out.append(row[3])

future_data=projdata

#Opening the calculated SRS or other measurement file
srs_data=[]
##obtaining ranks - choose ranking method based on user input
#Automatic model selection using Burke rating model
print('Model selection: ')
print('Model 1: Points')
print('Model 2: Burke (accounts for SoS and home strength)')
model_selection=2 #Need to retune burke calc
print('Automatic mode, model selection is 2, Burke')
if model_selection==1:
	model_csv='analytics/adj_pts_diff_vector.csv'
	model_function=pts_regress
        model_str='Points'
if model_selection==2:
	model_csv='burke_vector.csv'
	model_function=burke_regress
        model_str='Burke Rating'

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
	
	#what is the win percentage?
	winpct_data.append(model_function(dsrs))	




future_out=list(zip(home_out, away_out, dsrs_data, winpct_data)) 
	
#Part Two: Write out the "prediction" file.
csvfile_out = open(wkdir+'outfile_mcsims.csv','wb')
csvwriter = csv.writer(csvfile_out)
for row in future_out:
	#Only need to print the visiting and home team scores and names.
	csvwriter.writerow(row)
csvfile_out.close()

#Print a "fancy/human readable" version of the above
fancy_out=list(zip(date_out,home_out, away_out, dsrs_data, winpct_data))
fancy_out=[[row[0],team_abbreviation(row[1]),team_abbreviation(row[2]),row[3],row[4]] for row in fancy_out]
csvfile_out = open(wkdir+'coming_games_Excel.csv','wb')
csvwriter = csv.writer(csvfile_out)
csvwriter.writerow(['Date','Home Team','Away Team','Away Differential','Away Team Win Probability'])
for row in fancy_out:
	#Only need to print the visiting and home team scores and names.
	csvwriter.writerow(row)
csvfile_out.close()

print('Binomial win percentages have been calculated.')

#Output a formatted file that you can show and view easily - Write an xlsx
workbook=xlsxwriter.Workbook('Future_Games_Report_'+now_str+'.xlsx')
worksheet=workbook.add_worksheet()

#bold format for headers and appropriate widths
bold14=workbook.add_format({'bold':True,'font_size':14})
bold14.set_align('center')
bold14.set_align('vcenter')
bold14.set_text_wrap()

worksheet.set_column('A:A',22)
worksheet.set_column('B:B',15)
worksheet.set_column('C:C',15)
worksheet.set_column('D:D',15)
worksheet.set_column('E:E',15)

#Centering
centformat=workbook.add_format()
centformat.set_align('center')

#Number formats
diffformat=workbook.add_format()
pctformat=workbook.add_format()

diffformat.set_num_format('0.00')
pctformat.set_num_format('0.00%')

diffformat.set_align('center')
pctformat.set_align('center')

#Add headers to the xlsx.
worksheet.write('A1','Date',bold14)
worksheet.write('B1','Home Team',bold14)
worksheet.write('C1','Away Team',bold14)
worksheet.write('D1','Away - Home\n '+model_str+' \nDifferential',bold14)
worksheet.write('E1','Away Team\n Win Probability',bold14)

row=1
col=0

#Write the data
for date,ht,at,diff,prob in (fancy_out):
  col=0
  worksheet.write(row,col,date)
  worksheet.write(row,col+1,ht,centformat)
  worksheet.write(row,col+2,at,centformat)
  worksheet.write(row,col+3,diff,diffformat)
  worksheet.write(row,col+4,prob,pctformat)
  row += 1

#conditional formatting
worksheet.conditional_format('E2:E'+str(len(fancy_out)),{'type':'3_color_scale'})

workbook.close()

	
