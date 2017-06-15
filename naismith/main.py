#MAM - 16 Jan 16 

#Main control script.

print('Now on GIT, and GitHub, as of June 2017!')
print("""Even better, it's just one single folder!""")

import os
wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

def standings_generation():
  execfile(wkdir+'season_games_splitter.py')
  print("""Season splitting complete""")
  execfile(wkdir+'ratings_calculations.py')
  print("""Ratings calculations complete""")
  execfile(wkdir+'monte_carlo_calculations.py')
  print("""Binomial win percentages calculated""")

if __name__=='__main__':
    print("""Martin's Standings Projection Program V1.3""")
    standings_generation()
    print("Two options exist for Monte Carlo simulation:")
    print("""**Loop-based Monte-Carlo simulation (also returns playoff probabilities) """)
    print("""**Vectorized Monte-Carlo simulation (May be killed if n>too large for system. No playoff probabilities)""")
    mc_choice=raw_input("""Choose one of the following options (Loop/Vectorized): """)
    if mc_choice=='Loop':
        execfile(wkdir+'loop_monte_carlo.py')
    elif mc_choice=='Vectorized':
        execfile(wkdir+'vectorized_monte_carlo.py')
    else:
        print("""Invalid choice made. Please run one of the two files if desired later""")
    

