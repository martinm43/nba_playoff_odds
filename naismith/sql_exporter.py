#-*-coding:utf8;-*-
#qpy:2
#qpy:console

print "This is a SQL script executor"
db_folder='/storage/emulated/0/download/'
sql_folder='/storage/emulated/0/qpython/scripts/'

import sqlite3,os
from pprint import pprint

#CSV output function
#Part Two: Write out a file containing all games played
def list_to_csv(csvfile,list_of_lists):
    import csv
    csvfile_out = open(csvfile,'wb')
    csvwriter = csv.writer(csvfile_out)
    for row in list_of_lists:
        #Only need to print the visiting and home team scores and names.
        csvwriter.writerow(row)
    csvfile_out.close()
    return 1

conn=sqlite3.connect(os.path.join(db_folder,'nba_data_test.sqlite'))
c=conn.cursor()

print 'SQL script executor'
str_input=''
folder='/storage/emulated/0/download/'
csvfilename='results.csv'


with open(sql_folder+'query.sql', 'r') as myfile: 
  data=myfile.read().replace('\n', '')

  
str_input=data

if str_input.find('drop')==-1:
  query_result=c.execute(str_input).fetchall()
  pprint(query_result)

list_to_csv(folder+csvfilename,query_result)


  

conn.close()
