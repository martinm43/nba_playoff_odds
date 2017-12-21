#MAM - 24 Sep 2016
#Adding models from another file.

#Parsing data obtained from basketball-reference.com 
#for use in analyses. Data to be used for Monte Carlo simulation.

#Replace Excel Program with Python routine. Get what you need.
import csv,os,xlsxwriter
from analytics.morey import SRS_regress,burke_regress,pts_regress
from teamind.teamind import teamind
from string_conversion_tools import team_abbreviation

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

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

#Output a formatted file that you can show and view easily

#import os
#cwd=os.getcwd()+'/'

#import sqlite3

c=conn.cursor()

#Write an xlsx
#workbook=xlsxwriter.Workbook('Future_Games_Report.xlsx')
#worksheet=workbook.add_worksheet()

#bold format for headers and appropriate widths
#bold14=workbook.add_format({'bold':True,'font_size':14})
#bold14.set_align('center')
#worksheet.set_column('A:A',70)
#worksheet.set_column('B:B',20)
#worksheet.set_column('C:C',20)

#Cash formatting
#cashformat=workbook.add_format()
#cashformat.set_num_format(0x2c)
#cashformat.set_align('center')

#Centering
#centformat=workbook.add_format()
#centformat.set_align('center')

#Add headers to the xlsx.
worksheet.write('A1','Name',bold14)
worksheet.write('B1','Sugar (g/L)',bold14)
worksheet.write('C1','Volume (ml)',bold14)
worksheet.write('D1','Price',bold14)

row=1
col=0

#Write the data
# for name,sugar,volume,price in (data):
 # worksheet.write(row,col,name)
 # worksheet.write(row,col+1,sugar,centformat)
 # worksheet.write(row,col+2,volume,centformat)
 # worksheet.write(row,col+3,price/100.0,cashformat)
 # row += 1


#workbook.close()

	
