 
#Main control script.

import os
wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

def standings_generation():
  execfile(wkdir+'nba_api_team_indexer.py')
  print("""Game linking and team indexing complete""")
  execfile(wkdir+'season_games_splitter.py')
  print("""Season splitting complete""")
  execfile(wkdir+'analytics/ptsaverages.py')
  print("""Team point differentials high and low pass filtered and adjusted for home court advantage""")
  execfile(wkdir+'ratings_calculations.py')
  print("""Ratings calculations complete""")
  execfile(wkdir+'monte_carlo_calculations.py')
  print("""Binomial win percentages calculated""")

if __name__=='__main__':
    print("""Standings Projection Program V1.3""")
    standings_generation()    

