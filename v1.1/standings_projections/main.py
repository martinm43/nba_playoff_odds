#!/usr/bin/python

print('Analytics Program')
#MAM - 9 Oct 2016

#Run analysis scripts and export the results to .csv files and an xlsx.
#Not compatible with anaconda - there must be replacement packages
#from pyexcel.cookbook import merge_all_to_a_book

app_dir = ''

def srspred():
  execfile(app_dir+'standings_projections.py')
  execfile(app_dir+'ratings_calculations.py')
  execfile(app_dir+'monte_carlo_calculations.py')
  execfile(app_dir+'monte_carlo_simulation.py')

srspred()    

#merge_all_to_a_book(['MC_sim_results_Excel.csv','coming_games_Excel.csv'],'output_summary.xlsx')
