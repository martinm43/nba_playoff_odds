#-*-coding:utf8;-*-
#qpy:2

import sqlite3,os
from pprint import pprint

cwd=os.getcwd()+'/'

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

conn=sqlite3.connect(os.path.join(cwd,'lcbo_db.sqlite'))
c=conn.cursor()

csvfilename='results.csv'

with open(cwd+'query.sql', 'r') as myfile: 
  data=myfile.read().replace('\n', '')

  
str_input=data

if str_input.find('drop')==-1:
  query_result=c.execute(str_input).fetchall()
  pprint(query_result)

list_to_csv(cwd+csvfilename,query_result)


  

conn.close()
