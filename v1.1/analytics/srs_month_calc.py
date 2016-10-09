from access_nba_data import epochtime
from srscalc import srs_month_since_date
from dbtools import create_db,col_creator,insert_data
from season_dates import get_start_date,get_end_date
from pprint import pprint

#initial prototyping
#analysis_date=raw_input('Please enter a date: ')
#analysis_secs=epochtime(analysis_date)
#print(srs_month_since_date(analysis_secs))

#Create table
folder='/storage/emulated/0/download/'
dbname='nba_data_test.sqlite'
tablename='srs_table'
create_db(folder+dbname,tablename)

start_year=1997 #2005 on only because of 'lack of teams'
end_year=2017

#Full SRS List
full_srs_list=[]

#insertion counter
insert_no=1

#columns inserted flag
columns_insert=False

#For each season:
for year in range(start_year,end_year):
  #Get season start and end date. Start one
  #month from start date
  start_date=get_start_date(year)
  end_date=get_end_date(year)+86400 #include all dates
  calc_start_date=30*86400+start_date

  #Calculate 1-month srs while date < season_end_date
  calc_date=calc_start_date
  season_srs_list=[]

  while calc_date < end_date:
    resultslist=srs_month_since_date(calc_date)
    if calc_date==calc_start_date and year==start_year:
      col_creator(folder+dbname,tablename,resultslist[0])
    for k in resultslist:
      k['id']=insert_no
      #if calc_date==calc_start_date:
      #  col_creator(folder+dbname,tablename,resultslist[0])
      full_srs_list.append(k)
      insert_no+=1
    calc_date=calc_date+86400 #every week

for entry in full_srs_list:
  insert_data(folder+dbname,tablename,entry)