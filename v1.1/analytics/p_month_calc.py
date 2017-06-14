
from pprint import pprint

#analytics in folder
from season_dates import get_start_date,get_end_date
from access_nba_data import epochtime
from pdiffcalc import p_month_since_date

import sys
sys.path.append(app_dir+'v1.0_dev/python_db_tools/')
from dbtools import create_db,col_creator,insert_data



#initial prototyping
#analysis_date=raw_input('Please enter a date: ')
#analysis_secs=epochtime(analysis_date)
#print(srs_month_since_date(analysis_secs))

#Create table
db_folder='v1.0_dev/db_folder/'
dbname='nba_data_test.sqlite'
tablename='p_table'
create_db(db_folder+dbname,tablename)

start_year=1997 #2005 on only because of 'lack of teams'
end_year=2017

#Full P List
full_p_list=[]

#insertion counter
insert_no=1

#columns inserted flag
columns_insert=False

#For each season:
for year in range(start_year,end_year):
  print 'Performing calculations for year '+str(year)
  #Get season start and end date. Start one
  #month from start date
  start_date=get_start_date(year)
  print year,start_date
  end_date=get_end_date(year)+86400 #include all dates
  calc_start_date=30*86400+start_date

  #Calculate 1-month point diff while date < season_end_date
  calc_date=calc_start_date
  season_p_list=[]

  while calc_date < end_date:
    resultslist=p_month_since_date(calc_date)
    if calc_date==calc_start_date and year==start_year:
      col_creator(db_folder+dbname,tablename,resultslist[0])
    for k in resultslist:
      k['id']=insert_no
      #if calc_date==calc_start_date:
      #  col_creator(folder+dbname,tablename,resultslist[0])
      full_p_list.append(k)
      insert_no+=1
    calc_date=calc_date+86400*7.0 #every week

print 'Preparing to insert data'

for entry in full_p_list:
  insert_data(db_folder+dbname,tablename,entry)
