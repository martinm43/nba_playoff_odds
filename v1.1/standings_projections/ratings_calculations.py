#Project for 16 Jan 16
#SRS Calculations in Python
#See Doug Driner's definition of SRS as it applies in the NFL.
#This version is going to have straight calculations, nothing fancy.

#MAM

#from pprint import pprint
import csv

app_dir='/home/martin/naismith/v1.1/'
import sys
sys.path.append(app_dir+'analytics/')
from srscalc import srscalc
from burke_solver import burke_calc

srsdata=[]
phone='/home/martin/naismith/v1.1/standings_projections/'
print('Calculating models')
target='outfile_gms.csv'
  
with open(phone+target,'rb') as csvfile:
	balldata = csv.reader(csvfile,delimiter=',')
	for row in balldata:
		srsdata.append(row)
csvfile.close

#Convert the data into integers (this will not be necessary if using DB data)
srsdata=[[int(m) for m in l] for l in srsdata]

#Calculate SRS via blow-up proof approximation.
srsdicts=srscalc(srsdata)

#Calculate Burke SRS
burke_data=[[s[2],s[0],s[3],s[1]] for s in srsdata]
burkelist=burke_calc(burke_data)
burkelist=[[b] for b in burkelist]

#Print results to screen
print('Calculated SRS results via SVD:')
for s in srsdicts:
  print('Team '+str(s['team_id'])+', SRS (SVD approx): '+str(s['srs']))

#SRS_vector for writing to file
SRS_vector=[[s['srs']] for s in srsdicts]
#print SRS_vector

#write it out.
csvfile_out = open(phone+'SRS_vector.csv','wb')
csvwriter = csv.writer(csvfile_out)
for row in SRS_vector:
	#Only need to print the visiting and home team scores and names.
	csvwriter.writerow(row)
csvfile_out.close()

#write out burke vector
csvfile_out = open(phone+'burke_vector.csv','wb')
csvwriter = csv.writer(csvfile_out)
for row in burkelist:
	#Only need to print the visiting and home team scores and names.
	csvwriter.writerow(row)
csvfile_out.close()
