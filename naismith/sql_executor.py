#-*-coding:utf8;-*-
#qpy:2
#qpy:console

print "This is a SQL script executor"
db_folder='/storage/emulated/0/download/'
sql_folder='/storage/emulated/0/qpython/scripts/'

import sqlite3,os
from pprint import pprint

conn=sqlite3.connect(os.path.join(db_folder,'nba_data_test.sqlite'))
c=conn.cursor()

print 'SQL script executor'
str_input=''

with open(sql_folder+'query.sql', 'r') as myfile: 
  data=myfile.read().replace('\n', '')

  
str_input=data

if str_input.find('drop')==-1:
  pprint(c.execute(str_input).fetchall())


  

conn.close()
