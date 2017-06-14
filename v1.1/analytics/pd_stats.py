#-*-coding:utf8;-*-
#qpy:2
#qpy:console

print "This is console module"

phone=''

import scipy.stats as stats
import numpy as np
import sqlite3
from pprint import pprint

conn=sqlite3.connect(phone+'nba_data_test.sqlite')
c=conn.cursor()

print 'SQL explorer'
print 'Press END to quit'
str_input='SELECT point_diff FROM srs_table'
result=c.execute(str_input).fetchall()

#Stats
avg=np.average(result)
stddev=np.std(result)
length=len(result)
print(stats.normaltest(result))
