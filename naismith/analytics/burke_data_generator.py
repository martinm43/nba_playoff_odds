#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Generating data to be stored in a table for the purposes of generating a 
binomial regression model of NBA wins based on - for now - the one "Burke calc" factor
"""
import numpy as np
import matplotlib.pyplot as plt
from access_nba_data import games_query, epochtime
from burke_solver import burke_calc

import os
from dbtools import table_initializer
cwd=os.getcwd()+'/'
table_name='burke_calc_data'
dbname='nba_data.sqlite'

#Moving averages, via StackOverflow
def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]

#set start date and date related variables

start_year=1996
end_year=1998

burke_dicts_array=[]

for year_num in range(start_year,end_year):
#    Note: this code does not work in lockout years!
    year=str(year_num)
    new_year_num=year_num+1
    new_year=str(new_year_num)

    start_date=epochtime('Dec 1 '+year)
    end_date=epochtime('May 1 '+new_year)
    
    #Lockout manual overrides
#    start_date=epochtime('Dec 1 1996')
#    end_date=epochtime('May 5 1999')
    calc_date=start_date
    daysecs=24*60*60
    monthsecs=daysecs*30
    
    #placeholder array
    all_burke_calcs=[]

    while calc_date < end_date:
        temp_burke_calc=burke_calc(games_query(calc_date-monthsecs*3,calc_date),impmode='bballref')
        #For legacy data used from bballref_scores
        #temp_burke_calc=burke_calc(games_query(calc_date-monthsecs*3,calc_date))
        all_burke_calcs.append(temp_burke_calc)
        calc_date+=daysecs
    
    all_burke_calcs=np.asarray(all_burke_calcs)

    #151 days are measured in the array, each day corresponds to one day (or the amount of daysecs)
    #added to the "epochtime" of the first day.
    #Create a dict for the addition of these values to tables
    
    burke_rank_id=0
    for i in range (0, len(all_burke_calcs)):
        for j in range(0,30):
            burke_dict={}
            burke_dict['id']=year_num*10000+burke_rank_id
            burke_dict['date']=start_date+i*daysecs
            burke_dict['burke_ranking']=all_burke_calcs[i,j]
            burke_dict['team']=j
            burke_dicts_array.append(burke_dict)
            burke_dict['year']=year
            del(burke_dict)
            burke_rank_id+=1
    
    print(len(burke_dicts_array))
    print(year_num)
        

#Storing data in file using historical database table creation tools
table_initializer(cwd+dbname,table_name,burke_dicts_array[0],burke_dicts_array,automode='on')

#Plots for visually examining the "burkse calc" plots in question
#plot_team_id=0
#plt.plot(all_burke_calcs[:,plot_team_id])
##plt.plot(ave_burke_calcs[:,plot_team_id])
#plt.ylabel('team Burke score')
#plt.xlabel('days since tracking began')
#plt.show()
    

    
