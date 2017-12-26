"""
Main file for running the Future Games Projector, Standings Projector, and 
Playoff Odds Calculator sub-scripts.
""" 
import os
working_directory = os.path.dirname(os.path.realpath(__file__))+'/'

def standings_generation():
    "This function runs all the sub-scripts for the program"
    execfile(working_directory+'nba_api_team_indexer.py') #script is already automatic
    execfile(working_directory+'season_games_splitter.py') #need to figure out "how to figure out what year next May is in"
    execfile(working_directory+'analytics/ptsaverages.py') 
    execfile(working_directory+'ratings_calculations.py')
    execfile(working_directory+'monte_carlo_calculations.py')
    execfile(working_directory+'loop_monte_carlo.py')

if __name__ == '__main__':
    print 'Standings Projector and Playoffs Odds Calculator, v1.0'
    print 'MA Miller, 2017'
    standings_generation()
